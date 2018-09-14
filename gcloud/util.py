import hashlib

def generate_file_name(image_bytes):
    m = hashlib.blake2s()
    m.update(image_bytes)
    return '{}.jpg'.format(m.hexdigest())