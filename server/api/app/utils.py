import hashlib
import random
import string


def hash_string(filename):
    md5_hash = hashlib.md5()
    md5_hash.update(filename.encode('UTF-8'))
    return md5_hash.hexdigest()


def hash_file(filepath):
    md5_hash = hashlib.md5()
    with open(filepath, 'rb') as f:
        buf = f.read(65536)
        while len(buf) > 0:
            md5_hash.update(buf)
            buf = f.read(65536)
    return md5_hash.hexdigest()


def random_key(length=10):
    return ''.join(
        random.SystemRandom().choice(
            string.ascii_letters + string.digits
        ) for _ in range(length))
