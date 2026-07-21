from cryptography.fernet import Fernet

class EncryptionService:
    def __init__(self, encryption_key):
        self._key = encryption_key

        self._fernet = Fernet(self._key)

    
    def encrypt(self, data: str | int) -> str:
        return self._fernet.encrypt(str(data).encode('utf-8')).decode('utf-8')
    
    def decrypt(self, encrypted: str) -> str:
        return self._fernet.decrypt(encrypted.encode('utf-8')).decode('utf-8')

