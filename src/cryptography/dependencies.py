from fastapi import Request
from .types import EncryptionService, HashingService


def get_encryption_service(request: Request) -> EncryptionService:
    service = getattr(request.app.state, "ecryption_service", None)

    if not service:
        raise ValueError("No encryption service initialized in app")
    
    return service

def get_hashing_service(request: Request) -> HashingService:
    service = getattr(request.app.state, "hashing_service", None)

    if not service:
        raise ValueError("No hashing service initialized in app")
    
    return service