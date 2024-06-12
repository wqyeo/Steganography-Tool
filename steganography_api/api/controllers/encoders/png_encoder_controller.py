import random
import hashlib

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

def check_bits_usage(r_bits_usage, g_bits_usage, b_bits_usage):
    """
    Helper function to check if the bits used are valid or not...

    Will see if at least all 3 bits are not empty,
    they are within 0~7,
    no repeated bits for a single color...
    """
    if any(bits_usage != [] and (max(bits_usage) > 7 or min(bits_usage) < 0) for bits_usage in [r_bits_usage, g_bits_usage, b_bits_usage]):
        return False
    if any(len(set(bits_usage)) != len(bits_usage) for bits_usage in [r_bits_usage, g_bits_usage, b_bits_usage]):
        return False
    return True

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

def _set_image_bits_by_coordinates(image, row, col, r_bits_usage, g_bits_usage, b_bits_usage, binary_secret_data, data_index, data_len):
    """
    Helper function to set the bits of the image, based on the coordinates and rgb bits to use.

    Returns:
    -  image: updated image
    -  data_index: updated data index
    """
    pixel = image[row, col]
    r, g, b = list(to_bin(pixel[0])), list(to_bin(pixel[1])), list(to_bin(pixel[2]))

    # Modify red channel bits based on r_bits_usage
    for r_bit in r_bits_usage:
        if data_index < data_len:
            r[r_bit] = binary_secret_data[data_index]
            data_index += 1

    # Modify green channel bits based on g_bits_usage
    for g_bit in g_bits_usage:
        if data_index < data_len:
            g[g_bit] = binary_secret_data[data_index]
            data_index += 1

    # Modify blue channel bits based on b_bits_usage
    for b_bit in b_bits_usage:
        if data_index < data_len:
            b[b_bit] = binary_secret_data[data_index]
            data_index += 1

    # Combine modified channels and update pixel value
    pixel[0] = int(''.join(r), 2)
    pixel[1] = int(''.join(g), 2)
    pixel[2] = int(''.join(b), 2)

    image[row, col] = pixel
    return [image, data_index]

def _string_to_seed(seed_string):
    """
    Convert the string to an integer using a cryptographic hash function
    """
    hash_object = hashlib.md5(seed_string.encode())
    return int(hash_object.hexdigest(), 16)

def _random_encode_png(image_path, secret_payload, ending_payload, r_bits_usage, g_bits_usage, b_bits_usage):
    """
    Encoding pixels based on deterministic random generator, using the ending payload as seed..
    
    If collision is detected, it will use the next available pixel...
    """
    image = cv2.imread(image_path)

    # Maximun number of bytes we can encode with...
    n_bytes_red = (image.shape[0] * image.shape[1] * len(r_bits_usage)) // 8
    n_bytes_green = (image.shape[0] * image.shape[1] * len(g_bits_usage)) // 8
    n_bytes_blue = (image.shape[0] * image.shape[1] * len(b_bits_usage)) // 8
    n_bytes = n_bytes_red + n_bytes_green + n_bytes_blue

    if len(secret_payload + ending_payload) > n_bytes:
        raise ValueError("Insufficient bytes, use a smaller secret payload or a bigger image!")
    
    data_index = 0
    binary_secret_data = to_bin(secret_payload + ending_payload)

    # Length of the payload to hide
    data_len = len(binary_secret_data)

    used_numbers = set()

    seed = _string_to_seed(ending_payload)
    random_generaator = random.Random(seed)

    max_random_number = (image.shape[0] * image.shape[1]) - 1
    while data_index < data_len:
        current_number = random_generaator.randint(0, max_random_number)
        # Use the next free pixel, if already occupied.
        while current_number in used_numbers:
            current_number += 1
            current_number = current_number % max_random_number

        row, col = _get_pixel_coordinates(image, current_number)

        response = _set_image_bits_by_coordinates(image, row, col, r_bits_usage, g_bits_usage, b_bits_usage, binary_secret_data, data_index, data_len)
        image = response[0]
        data_index = response[1]
        used_numbers.add(current_number)
    return image



def _fibonacci_encode_png(image_path, secret_payload, ending_payload, r_bits_usage, g_bits_usage, b_bits_usage):
    """
    Encoding pixels based on fibonacci location.
    
    Upon reaching the end, it will loop back around to `1`.
    If collision is detected, it will use the next available pixel...
    """
    image = cv2.imread(image_path)

    # Maximun number of bytes we can encode with...
    n_bytes_red = (image.shape[0] * image.shape[1] * len(r_bits_usage)) // 8
    n_bytes_green = (image.shape[0] * image.shape[1] * len(g_bits_usage)) // 8
    n_bytes_blue = (image.shape[0] * image.shape[1] * len(b_bits_usage)) // 8
    n_bytes = n_bytes_red + n_bytes_green + n_bytes_blue

    if len(secret_payload + ending_payload) > n_bytes:
        raise ValueError("Insufficient bytes, use a smaller secret payload or a bigger image!")
    
    data_index = 0
    binary_secret_data = to_bin(secret_payload + ending_payload)

    # Length of the payload to hide
    data_len = len(binary_secret_data)

    current_seqence = [0, 1]
    used_numbers = set()
    current_number = 0
    while data_index < data_len:
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

        response = _set_image_bits_by_coordinates(image, row, col, r_bits_usage, g_bits_usage, b_bits_usage, binary_secret_data, data_index, data_len)
        image = response[0]
        data_index = response[1]
        used_numbers.add(current_number)
    return image



def _linear_encode_png(image_path, secret_payload, ending_payload, r_bits_usage, g_bits_usage, b_bits_usage):
    """
    linear encoding (top-left to bottom-right)
    """
    image = cv2.imread(image_path)

    # Maximun number of bytes we can encode with...
    n_bytes_red = (image.shape[0] * image.shape[1] * len(r_bits_usage)) // 8
    n_bytes_green = (image.shape[0] * image.shape[1] * len(g_bits_usage)) // 8
    n_bytes_blue = (image.shape[0] * image.shape[1] * len(b_bits_usage)) // 8
    n_bytes = n_bytes_red + n_bytes_green + n_bytes_blue

    if len(secret_payload + ending_payload) > n_bytes:
        raise ValueError("Insufficient bytes, use a smaller secret payload or a bigger image!")
    
    data_index = 0
    binary_secret_data = to_bin(secret_payload + ending_payload)

    # Length of the payload to hide
    data_len = len(binary_secret_data)
    for row in image:
        for pixel in row:
            r, g, b = list(to_bin(pixel[0])), list(to_bin(pixel[1])), list(to_bin(pixel[2]))

            # Modify red channel bits based on r_bits_usage
            for r_bit in r_bits_usage:
                if data_index < data_len:
                    r[r_bit] = binary_secret_data[data_index]
                    data_index += 1

            # Modify green channel bits based on g_bits_usage
            for g_bit in g_bits_usage:
                if data_index < data_len:
                    g[g_bit] = binary_secret_data[data_index]
                    data_index += 1

            # Modify blue channel bits based on b_bits_usage
            for b_bit in b_bits_usage:
                if data_index < data_len:
                    b[b_bit] = binary_secret_data[data_index]
                    data_index += 1

            # Combine modified channels and update pixel value
            pixel[0] = int(''.join(r), 2)
            pixel[1] = int(''.join(g), 2)
            pixel[2] = int(''.join(b), 2)

            # Done encoding...
            if data_index >= data_len:
                break

    return image

def png_encoder_controller(image_path, secret_payload, ending_payload, r_bits_usage, g_bits_usage, b_bits_usage, generator_type):
    """
    Encodes a PNG image

    - image_path: Path to the image
    - secret_payload: The payload to hide
    - ending_payload: Ending signal for payload
    - r_bits_usage: Which bits to use for red during encoding
    - g_bits_usage: Which bits to use for green during encoding
    - b_bits_usage: Which bits to use for blue during encoding
    (7 is MSB, 0 is LSB)
    - generator_type: Either 'linear', 'random' or 'fibonacci

    Returns the image.
    Raises `TypeError` if bad image
    Raises `ValueError` is the image is too small for the payload

    DOES NOT VALIDATE IF THE BITS USAGE ARE VALID OR NOT, USE `check_bits_usage` BEFORE INVOKING THIS
    """

    if generator_type == "linear":
        return _linear_encode_png(image_path, secret_payload, ending_payload, r_bits_usage, g_bits_usage, b_bits_usage)

    if generator_type == "fibonacci":
        return _fibonacci_encode_png(image_path, secret_payload, ending_payload, r_bits_usage, g_bits_usage, b_bits_usage)

    if generator_type == "random":
        return _random_encode_png(image_path, secret_payload, ending_payload, r_bits_usage, g_bits_usage, b_bits_usage)

    print(f"Bad generator type: {generator_type}; Defaulting to linear", flush=True)
    return _linear_encode_png(image_path, secret_payload, ending_payload, r_bits_usage, g_bits_usage, b_bits_usage)