from hashlib import md5
def hash(password):
    return md5(password.encode()).hexdigest()