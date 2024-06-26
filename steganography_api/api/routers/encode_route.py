import sys
import traceback
import json
import magic
import cv2
import tempfile
from pathlib import Path
import uuid as uuidgen

from django.core.files import File
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import os

from ..models import FileModel
from ..utils.is_valid_file import is_valid_file
from ..controllers.encoders.png_encoder_controller import png_encoder_controller
from ..controllers.encoders.wav_encoder_controller import wav_encoder_controller

def _handle_save_png_image(image, matching_file):
    if image is None:
        return JsonResponse({'status': 'ERROR', 'message': 'Failed to encode the image.'}, status=500)

    # Create a temporary directory to store the temporary file
    new_file_instance = None
    with tempfile.TemporaryDirectory(dir="") as temp_dir:
        temp_dir_name_without_prefix = temp_dir.replace('/app/', '')

        file_name = "encoded_" + matching_file.file_name
        temp_file_path = os.path.join(temp_dir_name_without_prefix, file_name)
        cv2.imwrite(str(temp_file_path), image)

        # Open the temporary file and save it to a new FileModel instance
        with open(temp_file_path, 'rb') as f:
            new_file = File(f)
            new_file_instance = FileModel(
                file=new_file,
                encoded_from=matching_file,
                file_type='image/png',
                file_name=file_name
            )
            new_file_instance.save()
        

    return JsonResponse({
        'status': 'SUCCESS',
        'message': 'Successfully encoded the image',
        'file_uuid': str(new_file_instance.id)
    }, status=200)


# Function to validate the bits array
def _validate_bits(bits):
    if not isinstance(bits, list):
        return False
    if not all(isinstance(x, int) and 0 <= x <= 7 for x in bits):
        return False
    if len(bits) != len(set(bits)):
        return False
    return True

@csrf_exempt
def encode_file(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'ERROR'}, status=404)

    try:
        file_id = request.POST.get("file_uuid")
        secret_key = request.POST.get("secret_key")
        message = request.POST.get("message")
        generator_type = request.POST.get("generator_type", "linear")

        # Check if any of these are left empty/blank
        if not file_id or not secret_key or not message:
            return JsonResponse({'status': 'MISSING_FIELDS', 'message': 'Required fields are missing.'}, status=400)
        matching_file = get_object_or_404(FileModel, id=file_id)

        # Determine file type, and determine encoding function to use.
        file_path = matching_file.file.path
        mime = magic.Magic(mime=True)
        mime_type = mime.from_file(file_path)

        if mime_type == 'image/png':
            # Image file, validate if r/g/b bits are filled.
            r_bits = json.loads(request.POST.get("r_bits", "[]"))
            g_bits = json.loads(request.POST.get("g_bits", "[]"))
            b_bits = json.loads(request.POST.get("b_bits", "[]"))

            if not r_bits and not g_bits and not b_bits:
                return JsonResponse({'status': 'MISSING_FIELDS', 'message': 'At least one bit array should be provided.'}, status=400)

            if not _validate_bits(r_bits) or not _validate_bits(g_bits) or not _validate_bits(b_bits):
                return JsonResponse({'status': 'BAD_BITS', 'message': 'Bits arrays must be unique integers between 0 and 7.'}, status=400)

            image = png_encoder_controller(file_path, message, secret_key, r_bits, g_bits, b_bits, generator_type)
            return _handle_save_png_image(image, matching_file)
        elif mime_type == 'audio/wav' or mime_type == 'audio/x-wav':
            lsb_count = int(request.POST.get("lsb_count", "0"))
            if lsb_count < 0 or lsb_count >= 8:
                return JsonResponse({'status': 'BAD_BITS', 'message': 'lsb_count must be a integer between 0 and 7.'}, status=400)
            return wav_encoder_controller(message, secret_key, matching_file, lsb_count + 1)

        return JsonResponse({'status': 'UNIMPLEMENTED', 'message': 'An error occured. Likely trying to encode a unsupported file type!'}, status=500)
    except ValueError as e:
        return JsonResponse({'status': 'PAYLOAD_TOO_LARGE'}, status=400)
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__, file=sys.stderr, chain=True)
        sys.stderr.flush()
        print(f"Error occurred encoding file :: {e}", flush=True)
        return JsonResponse({'status': 'ERROR'}, status=500)
