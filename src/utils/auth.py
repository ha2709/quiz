from fastapi import Depends, HTTPException, WebSocket
from fastapi.security import OAuth2PasswordBearer

from src.services.user_service import UserService
from src.utils.dependencies import get_user_service
from src.utils.logger import LoggerSingleton
from src.utils.token import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
logger = LoggerSingleton().logger


async def validate_and_get_user(token: str, user_service: UserService):
    """
    Validates the token and fetches the user from the database.
    Reusable logic for both HTTP and WebSocket contexts.
    """
    try:
        token_data = decode_token(token)
        user_id = token_data.get("user_id")
    except ValueError as e:
        logger.error(f"Token validation error: {str(e)}")
        raise HTTPException(status_code=401, detail=str(e))

    user = await user_service.get_user_by_id(user_id)
    if not user:
        logger.warning(f"User not found with ID: {user_id}")
        raise HTTPException(status_code=404, detail="User not found")

    return user


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_service: UserService = Depends(get_user_service),
):
    """
    Retrieves the current user for HTTP requests.
    """
    return await validate_and_get_user(token, user_service)


async def get_current_user_for_ws(
    token: str,
    user_service: UserService,
):
    """
    Validate the token and retrieve the current user.
    """
    try:
        payload = decode_token(token)
        user_id = payload.get("user_id")
        if not user_id:
            logger.warning("Invalid token: missing user_id.")
            raise HTTPException(status_code=401, detail="Invalid token")

        user = await user_service.get_user_by_id(user_id)
        if not user:
            logger.warning(f"User not found with ID: {user_id}")
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except Exception as e:
        logger.error(f"Token validation error: {str(e)}")
        raise HTTPException(status_code=401, detail="Invalid token")
