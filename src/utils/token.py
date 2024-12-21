import os
from datetime import datetime, timedelta

import jwt

# from jwt import decode as pyjwt_decode
# from jwt import encode as pyjwt_encode
# from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))


def decode_token(token: str) -> dict:
    # try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    user_id = payload.get("user_id")
    username = payload.get("username")

    if user_id is None or username is None:
        raise ValueError("Token payload does not contain user_id or username.")

    return {"user_id": user_id, "username": username}

    # except ExpiredSignatureError:
    #     raise ValueError("Token has expired.")
    # except InvalidTokenError as e:
    #     raise ValueError(f"Invalid token: {e}")


def create_token(payload: dict) -> str:
    try:
        to_encode = payload.copy()
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire, "iat": datetime.utcnow()})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    except Exception as e:
        raise ValueError(f"Error creating token: {e}")
