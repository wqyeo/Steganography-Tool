import magic

def is_valid_file(file_type):
    return file_type in ["image/jpeg", "image/png", "image/gif", "video/mp4", "audio/mpeg"]