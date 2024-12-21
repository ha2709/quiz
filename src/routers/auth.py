from fastapi import APIRouter, Depends, Form, HTTPException

from src.services.user_service import UserService
from src.utils.dependencies import get_user_service
from src.utils.exceptions import (
    InvalidCredentialsException,
    UserAlreadyExistsException,
    UserNotFoundException,
)
from src.utils.response import format_response
from src.utils.token import create_token

router = APIRouter(tags=["auth"])


@router.post("/register")
async def register(
    username: str,
    password: str,
    user_service: UserService = Depends(get_user_service),
):
    try:
        new_user = await user_service.create_user(username, password)
        return format_response(
            "success",
            "User registered successfully.",
            {"id": new_user.id, "username": new_user.username},
        )
    except UserAlreadyExistsException as e:
        return format_response("error", str(e.detail))


@router.post("/login")
async def login(
    username: str,
    password: str,
    user_service: UserService = Depends(get_user_service),
):
    try:
        user = await user_service.authenticate_user(username, password)
        return format_response(
            "success", "Login successful.", {"id": user.id, "username": user.username}
        )
    except UserNotFoundException as e:
        return format_response("error", str(e.detail))
    except InvalidCredentialsException as e:
        return format_response("error", str(e.detail))


@router.post("/auth/token")
async def login_for_access_token(
    username: str = Form(...),
    password: str = Form(...),
    user_service: UserService = Depends(get_user_service),
):
    try:
        user = await user_service.authenticate_user(username, password)
        # print(51, user.username)
        token_payload = {"user_id": user.id, "username": user.username}
        access_token = create_token(token_payload)
        return format_response(
            "success",
            "Token generated successfully.",
            {"access_token": access_token, "token_type": "bearer"},
        )
    except UserNotFoundException:
        return format_response("error", str(e.detail))
    except InvalidCredentialsException:
        return format_response("error", "Invalid credentials.")
