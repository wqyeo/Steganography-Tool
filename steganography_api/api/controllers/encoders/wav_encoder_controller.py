import os
import wave
import tempfile
import numpy as np

from django.core.files import File
from django.http import JsonResponse

from ...models import FileModel

def wav_encoder_controller(text, secret_key, matching_file, lsb_count):
    """
    Original written by TPeiWen from https://github.com/TPeiWen/audio_stego

    text: Message to encode
    secret_key: Secret key to end the message with.
    matching_file: Original matching FileModel (WAV File)
    lsb_count: How many LSB bits to use up
    """

    full_text = text + secret_key
    with wave.open(matching_file.file.path, "rb") as audio_file:
        frames = audio_file.readframes(-1)
        frames = np.frombuffer(frames, dtype=np.int16)
        binary_text = "".join(format(ord(char), "08b") for char in full_text)
        text_index = 0
        encoded_frames = frames.copy()

        for i in range(len(encoded_frames)):
            for bit in range(lsb_count):
                if text_index < len(binary_text):
                    encoded_frames[i] = (encoded_frames[i] & ~(1 << bit)) | (int(binary_text[text_index]) << bit)
                    text_index += 1
                else:
                    break

    new_file_instance = None
    with tempfile.TemporaryDirectory(dir="") as temp_dir:
        temp_dir_name_without_prefix = temp_dir.replace('/app/', '')
        file_name = "encoded_" + matching_file.file_name
        temp_file_path = os.path.join(temp_dir_name_without_prefix, file_name)

        with wave.open(temp_file_path, "wb") as encoded_audio_file:
            encoded_audio_file.setparams(audio_file.getparams())
            encoded_audio_file.writeframes(encoded_frames.tobytes())

        # Open the temporary file and save it to a new FileModel instance
        with open(temp_file_path, 'rb') as f:
            new_file = File(f)
            new_file_instance = FileModel(
                file=new_file,
                encoded_from=matching_file,
                file_type=matching_file.file_type,
                file_name=file_name
            )
            new_file_instance.save()
    
    return JsonResponse({
        'status': 'SUCCESS',
        'message': 'Successfully encoded the WAV file',
        'file_uuid': str(new_file_instance.id)
    }, status=200)