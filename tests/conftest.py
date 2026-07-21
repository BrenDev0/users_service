import pytest
from unittest.mock import AsyncMock, Mock
from src.models import User
from uuid import uuid4
from datetime import datetime

@pytest.fixture
def mock_user():
    return User(
        id=uuid4(),
        email="encrypted",
        email_hash="dhashed",
        password="hashed",
        created_at=datetime.now()
    )

@pytest.fixture
def mock_create_user():
    return AsyncMock()


@pytest.fixture
def mock_encryption_service():
    return Mock()

@pytest.fixture
def mock_hashing_service():
    return Mock()

