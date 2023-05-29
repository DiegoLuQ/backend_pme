from passlib.hash import bcrypt


def hash_password(password):
    hashed_password = bcrypt.hash(password)
    return hashed_password


def verify_password(password, hashed_password):
    if bcrypt.verify(password, hashed_password):
        return True
    else:
        
        return False
