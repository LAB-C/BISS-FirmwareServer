import hashlib, random, string

def hash_string(filename):
    md5_hash = hashlib.md5()
    md5_hash.update(filename.encode('UTF-8'))
    return md5_hash.hexdigest()

def randomKey(length=30):
    return ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(length))
