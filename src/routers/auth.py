from fastapi import APIRouter, Depends, Form, HTTPException

from src.services.user_service import UserService
from src.utils.dependencies import get_user_service
from src.utils.exceptions import (
    InvalidCredentialsException,
    UserAlreadyExistsException,
    UserNotFoundException,
)
from src.utils.logger import LoggerSingleton
from src.utils.response import format_response
from src.utils.token import create_token

logger = LoggerSingleton().logger
router = APIRouter(tags=["auth"])


@router.post("/register")
async def register(
    username: str,
    password: str,
    user_service: UserService = Depends(get_user_service),
):
    try:
        logger.info(f"Registering user: {username}")
        new_user = await user_service.create_user(username, password)
        logger.info(f"User {username} registered successfully with ID: {new_user.id}")

        return format_response(
            "success",
            "User registered successfully.",
            {"id": new_user.id, "username": new_user.username},
        )
    except UserAlreadyExistsException as e:
        logger.error(f"user already existed {username}: {str(e)}")
        return format_response("error", str(e.detail))
    except Exception as e:
        logger.error(f"Error registering user {username}: {str(e)}")
        raise HTTPException(status_code=400, detail="Registration failed")


@router.post("/login")
async def login(
    username: str,
    password: str,
    user_service: UserService = Depends(get_user_service),
):
    try:
        logger.info(f"Attempting login for user: {username}")
        user = await user_service.authenticate_user(username, password)
        logger.info(f"Login successful for user: {username}")
        return format_response(
            "success", "Login successful.", {"id": user.id, "username": user.username}
        )
    except UserNotFoundException as e:
        logger.warning(f"Login failed - User not found: {username}")
        return format_response("error", "User not found.")
    except InvalidCredentialsException as e:
        logger.warning(f"Login failed - Invalid credentials for user: {username}")
        return format_response("error", "Invalid credentials.")
    except Exception as e:
        logger.error(f"Login failed for user {username}: {str(e)}")
        raise HTTPException(status_code=401, detail="Login failed")


@router.post("/auth/token")
async def login_for_access_token(
    username: str = Form(...),
    password: str = Form(...),
    user_service: UserService = Depends(get_user_service),
):
    try:
        logger.info(f"Generating token for user: {username}")
        user = await user_service.authenticate_user(username, password)
        logger.info(f"User authenticated for token generation: {username}")

        token_payload = {"user_id": user.id, "username": user.username}
        access_token = create_token(token_payload)

        logger.info(f"Token generated successfully for user: {username}")
        return format_response(
            "success",
            "Token generated successfully.",
            {"access_token": access_token, "token_type": "bearer"},
        )
    except UserNotFoundException as e:
        logger.warning(f"Token generation failed - User not found: {username}")
        return format_response("error", "User not found.")
    except InvalidCredentialsException as e:
        logger.warning(
            f"Token generation failed - Invalid credentials for user: {username}"
        )
        return format_response("error", "Invalid credentials.")
    except Exception as e:
        logger.error(f"Token generation failed for user {username}: {str(e)}")
        raise HTTPException(status_code=401, detail="Token generation failed")
