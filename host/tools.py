import hashlib

def get_md5(content):
    md1 = hashlib.md5(content)
    return md1.hexdigest()