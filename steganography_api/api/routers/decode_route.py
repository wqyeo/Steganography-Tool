import json
import magic
import cv2
import tempfile
from pathlib import Path
import uuid as uuidgen

from django.conf import settings
from django.core.files import File
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import os

from ..models import FileModel
from ..utils.is_valid_file import is_valid_file
from ..controllers.decoders.png_decoder_controller import png_decoder_controller

def _handle_decode_png_image(decoded_payload):
    if decoded_payload is None:
        return JsonResponse({'status': 'ERROR', 'message': 'Failed to decode the image.'}, status=500)
    return JsonResponse({'status': 'SUCCESS', 'message': 'Decoding is done.', 'found': decoded_payload['found'], 'decoded': decoded_payload['decoded']}, status=200)

@csrf_exempt
def decode_file(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'ERROR'}, status=404)

    try:
        file_id = request.POST.get("file_uuid")
        r_bits = json.loads(request.POST.get("r_bits", "[]"))  # Expecting JSON array in string format
        g_bits = json.loads(request.POST.get("g_bits", "[]"))
        b_bits = json.loads(request.POST.get("b_bits", "[]"))
        secret_key = request.POST.get("secret_key")
        generator_type = request.POST.get("generator_type", "linear")

        # Check if any of these are left empty/blank
        if not file_id or not secret_key:
            return JsonResponse({'status': 'MISSING_FIELDS', 'message': 'Required fields are missing.'}, status=400)

        # Validate if all 3 arrays are empty
        if not r_bits and not g_bits and not b_bits:
            return JsonResponse({'status': 'MISSING_FIELDS', 'message': 'At least one bit array should be provided.'}, status=400)

        # Function to validate the bits array
        def validate_bits(bits):
            if not isinstance(bits, list):
                return False
            if not all(isinstance(x, int) and 0 <= x <= 7 for x in bits):
                return False
            if len(bits) != len(set(bits)):
                return False
            return True

        if not validate_bits(r_bits) or not validate_bits(g_bits) or not validate_bits(b_bits):
            return JsonResponse({'status': 'BAD_BITS', 'message': 'Bits arrays must be unique integers between 0 and 7.'}, status=400)

        matching_file = get_object_or_404(FileModel, id=file_id)

        # Determine file type, and determine encoding function to use.
        file_path = matching_file.file.path
        mime = magic.Magic(mime=True)
        mime_type = mime.from_file(file_path)

        if mime_type == 'image/png':
            decoded_payload = png_decoder_controller(file_path, secret_key, r_bits, g_bits, b_bits, generator_type)
            return _handle_decode_png_image(decoded_payload)

        return JsonResponse({'status': 'ERROR', 'message': 'Unknown error, contact admin!'})
    except Exception as e:
        print(f"Error occurred decoding file :: {e}", flush=True)
        return JsonResponse({'status': 'ERROR'}, status=500)
