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
    - generator_type: Either 'linear' or 'fibonacci

    Returns the image.
    Raises `TypeError` if bad image
    Raises `ValueError` is the image is too small for the payload

    DOES NOT VALIDATE IF THE BITS USAGE ARE VALID OR NOT, USE `check_bits_usage` BEFORE INVOKING THIS
    """

    # TODO: Handle other generator types.
    return _linear_encode_png(image_path, secret_payload, ending_payload, r_bits_usage, g_bits_usage, b_bits_usage)