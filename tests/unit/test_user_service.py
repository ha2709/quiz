from unittest.mock import MagicMock

import pytest

from src.services.user_service import UserService
from src.utils.exceptions import UserAlreadyExistsException


def test_create_user_already_exists():
    mock_repo = MagicMock()
    mock_repo.get_user_by_username.return_value = object()  # simulate existing user
    user_service = UserService(mock_repo)

    with pytest.raises(UserAlreadyExistsException):
        user_service.create_user("existing_user", "password123")
