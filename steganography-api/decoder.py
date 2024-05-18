import cv2
import numpy as np

def to_bin(data):
    if isinstance(data, str):
        return ''.join([ format(ord(i), "08b") for i in data])
    elif isinstance(data, bytes) or isinstance(data, np.ndarray):
        return [ format(i, "08b") for i in data]
    elif isinstance(data, int) or isinstance(data, np.uint8):
        return format(data, "08b")
    else:
        raise TypeError("Type not supported!")

def decode_png(image_path, ending_payload, r_bits_usage, g_bits_usage, b_bits_usage):
    """
    Decodes a PNG image to extract hidden payload.

    - image: The encoded image
    - r_bits_usage: Which bits were used for red during encoding
    - g_bits_usage: Which bits were used for green during encoding
    - b_bits_usage: Which bits were used for blue during encoding

    Returns the extracted payload.
    """
    image = cv2.imread(image_path)

    extracted_payload = ""
    for row in image:
        for pixel in row:
            r, g, b = pixel[0], pixel[1], pixel[2]

            # Extract the specified bits from the red, green, and blue channels
            for r_bit in r_bits_usage:
                extracted_payload += str((r >> (7 - r_bit)) & 1)
            for g_bit in g_bits_usage:
                extracted_payload += str((g >> (7 - g_bit)) & 1)
            for b_bit in b_bits_usage:
                extracted_payload += str((b >> (7 - b_bit)) & 1)

    decoded_payload = "".join([chr(int(extracted_payload[i:i+8], 2)) for i in range(0, len(extracted_payload), 8)])
    # Find the ending payload and truncate the extracted payload
    end_index = decoded_payload.find(ending_payload)
    key_used = False
    if end_index != -1:
        key_used = True
        decoded_payload = decoded_payload[:end_index]

    return {
        "found": key_used,
        "decoded": decoded_payload
    }