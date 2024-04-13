from hashlib import md5
def hash(password):
    return md5(password.encode()).hexdigest()

if __name__ == '__main__':
    print(hash('test'))