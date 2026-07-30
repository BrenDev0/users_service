import os

os.environ.setdefault("DATABASE_URL", "postgresql+asyncpg://user:pass@localhost/test_db")
os.environ.setdefault("ENCRYPTION_KEY", "wnR9tBQCUEjhaqZeSQIauSPfd2FnJZ_wSj7wl1nH6d0=")
os.environ.setdefault("REDIS_URL", "redis://localhost:6379/0")

import pytest
from unittest.mock import AsyncMock, Mock
from src.users.models import User
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


@pytest.fixture
def mock_get_user_by_id():
    return AsyncMock()


@pytest.fixture
def mock_delete_user_by_id():
    return AsyncMock()


@pytest.fixture
def mock_cache_store():
    return AsyncMock()

