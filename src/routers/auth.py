from fastapi import APIRouter, Depends, Form, HTTPException

from src.services.user_service import UserService
from src.utils.dependencies import get_user_service
from src.utils.exceptions import (
    InvalidCredentialsException,
    UserAlreadyExistsException,
    UserNotFoundException,
)
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
        return {"id": new_user.id, "username": new_user.username}
    except UserAlreadyExistsException as e:
        raise HTTPException(status_code=400, detail=str(e.detail))


@router.post("/login")
async def login(
    username: str,
    password: str,
    user_service: UserService = Depends(get_user_service),
):
    try:
        user = await user_service.authenticate_user(username, password)
        return {"id": user.id, "username": user.username}
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e.detail))
    except InvalidCredentialsException as e:
        raise HTTPException(status_code=401, detail=str(e.detail))


@router.post("/auth/token")
async def login_for_access_token(
    username: str = Form(...),
    password: str = Form(...),
    user_service: UserService = Depends(get_user_service),
):
    try:
        user = await user_service.authenticate_user(username, password)
        token_payload = {"user_id": user.id, "username": user.username}
        access_token = create_token(token_payload)
        return {"access_token": access_token, "token_type": "bearer"}
    except UserNotFoundException:
        raise HTTPException(status_code=404, detail="User not found")
    except InvalidCredentialsException:
        raise HTTPException(status_code=401, detail="Invalid credentials")
