from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from src.services.user_service import UserService
from src.utils.dependencies import get_user_service
from src.utils.exceptions import UserNotFoundException
from src.utils.token import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_service: UserService = Depends(get_user_service),
):
    try:
        user_info = decode_token(token)
        user_id = user_info.get("user_id")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )

        user = await user_service.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundException()

        return user
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
