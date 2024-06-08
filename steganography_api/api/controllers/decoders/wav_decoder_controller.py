import os
import wave
import numpy as np

from django.core.files import File
from django.http import JsonResponse

from ...models import FileModel

def wav_decoder_controller(secret_key, target_file, lsb_count):
    """
    Original written by TPeiWen from https://github.com/TPeiWen/audio_stego

    secret_key: Secret key to end the message with.
    target_file: Target FileModel (WAV File)
    lsb_count: How many LSB bits to use up
    """
    with wave.open(target_file.file.path, "rb") as audio_file:
        frames = audio_file.readframes(-1)
        frames = np.frombuffer(frames, dtype=np.int16)

        binary_text = ""
        for frame in frames:
        # Extract the specified number of LSBs from each frame
            for i in range(lsb_count):
                binary_text += str((frame >> i) & 1)

        # Handle incomplete byte at the end if not divisible by 8
        if len(binary_text) % 8 != 0:
            binary_text = binary_text[:-(len(binary_text) % 8)]

        decoded_text = ""
        key_used = False
        i = 0
        while i < len(binary_text):
            byte = binary_text[i:i+8]
            decoded_text += chr(int(byte, 2))
            if decoded_text.endswith(secret_key):
                key_used = True
                decoded_text = decoded_text[:-len(secret_key)]
                break
            i += 8

        return {"decoded": decoded_text, "found": key_used}