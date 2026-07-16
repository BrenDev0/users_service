import bcrypt
import hashlib


class BcryptHashingService:
    def __init__(self):
        pass


    def hash_password(self, password: str) -> str:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    def compare_password(self, password: str, hashed_value: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), hashed_value.encode('utf-8'))
    

    def deterministic_hash(self, str_to_dhash: str) -> str:
        bytes = str_to_dhash.lower().encode('utf-8')
        dhashed = hashlib.sha256(bytes).hexdigest()

        return dhashed 
