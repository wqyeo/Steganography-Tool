import magic

def is_valid_file(file_type):
    return file_type in ["image/png", "audio/wav", "audio/x-wav"]