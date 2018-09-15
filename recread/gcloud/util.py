from recread.util import hash_bytes

def generate_file_name(image_bytes):
    return f'{hash_bytes(image_bytes)}.jpg'
