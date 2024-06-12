import hashlib
import random

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
    
def _get_pixel_coordinates(image, index):
    """
    Helper function to get the coordinates of the pixel
    (Where top-left is 0, bottom-right is the maximum possible value)
    """
    # Get the number of rows and columns
    num_columns = image.shape[1]
    
    # Calculate the row and column from the index
    row = index // num_columns
    col = index % num_columns
    
    return row, col

def _string_to_seed(seed_string):
    """
    Convert the string to an integer using a cryptographic hash function
    """
    hash_object = hashlib.md5(seed_string.encode())
    return int(hash_object.hexdigest(), 16)


def _random_decode_png(image_path, ending_payload, r_bits_usage, g_bits_usage, b_bits_usage):
    image = cv2.imread(image_path)

    read_count = 0
    max_possible_read_length = (image.shape[0] * image.shape[1]) -1

    seed = _string_to_seed(ending_payload)
    random_generator = random.Random(seed)
    used_numbers = set()

    extracted_payload = ""
    while read_count < max_possible_read_length:
        current_number = random_generator.randint(0, max_possible_read_length) 
        
        # Use the next free pixel, if already occupied.
        while current_number in used_numbers:
            current_number += 1
            current_number = current_number % max_possible_read_length

        used_numbers.add(current_number)
        row, col = _get_pixel_coordinates(image, current_number)

        pixel = image[row, col]
        r, g, b = bin(pixel[0])[2:].zfill(8), bin(pixel[1])[2:].zfill(8), bin(pixel[2])[2:].zfill(8)

        # Extract the specified bits from the red, green, and blue channels
        for r_bit in r_bits_usage:
            extracted_payload += r[r_bit]
        for g_bit in g_bits_usage:
            extracted_payload += g[g_bit]
        
        for b_bit in b_bits_usage:
            extracted_payload += b[b_bit]
         
        decoded_payload = "".join([chr(int(extracted_payload[i:i+8], 2)) for i in range(0, len(extracted_payload), 8)])
        end_index = decoded_payload.find(ending_payload)

        read_count += 1
        if end_index != -1:
            return {
                "found": True,
                "decoded": decoded_payload[:end_index]
            }
        
    del image
    decoded_payload = "".join([chr(int(extracted_payload[i:i+8], 2)) for i in range(0, len(extracted_payload), 8)])
    return {
        "found": False,
        "decoded": decoded_payload
    }



def _fibonacci_decode_png(image_path, ending_payload, r_bits_usage, g_bits_usage, b_bits_usage):
    image = cv2.imread(image_path)

    read_count = 0
    max_possible_read_length = (image.shape[0] * image.shape[1]) -1

    current_seqence = [0, 1]
    current_number = 1
    used_numbers = set()

    extracted_payload = ""
    while read_count < max_possible_read_length:
        current_number = current_seqence[0] + current_seqence[1]
        current_seqence[0] = current_seqence[1]
        current_seqence[1] = current_number
        
        # Use the next free pixel, if already occupied.
        while current_number in used_numbers:
            current_number += 1
        
        row, col = _get_pixel_coordinates(image, current_number)
        if col >= image.shape[1] or row >= image.shape[0]:
            # Out of bound, start looping around.
            current_seqence = [1, 1]
            current_number = 1
            # Use the next free pixel, if already occupied.
            while current_number in used_numbers:
                current_number += 1
            
            row, col = _get_pixel_coordinates(image, current_number)
        used_numbers.add(current_number)

        pixel = image[row, col]
        r, g, b = bin(pixel[0])[2:].zfill(8), bin(pixel[1])[2:].zfill(8), bin(pixel[2])[2:].zfill(8)

        # Extract the specified bits from the red, green, and blue channels
        for r_bit in r_bits_usage:
            extracted_payload += r[r_bit]
        for g_bit in g_bits_usage:
            extracted_payload += g[g_bit]
        
        for b_bit in b_bits_usage:
            extracted_payload += b[b_bit]

         
        decoded_payload = "".join([chr(int(extracted_payload[i:i+8], 2)) for i in range(0, len(extracted_payload), 8)])
        end_index = decoded_payload.find(ending_payload)


        read_count += 1
        if end_index != -1:
            return {
                "found": True,
                "decoded": decoded_payload[:end_index]
            }
        
    del image
    decoded_payload = "".join([chr(int(extracted_payload[i:i+8], 2)) for i in range(0, len(extracted_payload), 8)])
    return {
        "found": False,
        "decoded": decoded_payload
    }

def _linear_decode_png(image_path, ending_payload, r_bits_usage, g_bits_usage, b_bits_usage):
    image = cv2.imread(image_path)

    extracted_payload = ""
    for row in image:
        for pixel in row:
            r, g, b = bin(pixel[0])[2:].zfill(8), bin(pixel[1])[2:].zfill(8), bin(pixel[2])[2:].zfill(8)

            # Extract the specified bits from the red, green, and blue channels
            for r_bit in r_bits_usage:
                extracted_payload += r[r_bit]
            for g_bit in g_bits_usage:
                extracted_payload += g[g_bit]

            for b_bit in b_bits_usage:
                extracted_payload += b[b_bit]
    del image
    
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

def png_decoder_controller(image_path, ending_payload, r_bits_usage, g_bits_usage, b_bits_usage, generator_type):
    """
    Decodes a PNG image to extract hidden payload.

    - image: The encoded image
    - r_bits_usage: Which bits were used for red during encoding
    - g_bits_usage: Which bits were used for green during encoding
    - b_bits_usage: Which bits were used for blue during encoding

    Returns the extracted payload.
    """

    if generator_type == "fibonacci":
        return _fibonacci_decode_png(image_path, ending_payload, r_bits_usage, g_bits_usage, b_bits_usage)
    
    if generator_type == "linear":
        return _linear_decode_png(image_path, ending_payload, r_bits_usage, g_bits_usage, b_bits_usage)

    if generator_type == "random":
        return _random_decode_png(image_path, ending_payload, r_bits_usage, g_bits_usage, b_bits_usage)

    print(f"Unknown generator type of {generator_type}; Defaulting to linear", flush=True)
    return _linear_decode_png(image_path, ending_payload, r_bits_usage, g_bits_usage, b_bits_usage)