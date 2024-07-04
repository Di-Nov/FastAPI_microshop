from datetime import timedelta, datetime

import jwt
import bcrypt
from core.config import settings


def encode_jwt_token(
    payload: dict,
    private_key: str = settings.auth_jwt.private_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
    expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None,
):
    to_encode = payload.copy()
    now = datetime.utcnow()
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(
        exp=expire,
        # iet=now,
        iat=now.timestamp(),
        # iet=now.isoformat(),
    )
    encoded = jwt.encode(to_encode, private_key, algorithm)
    return encoded


def decode_jwt_token(
    token: str | bytes,
    public_key: str = settings.auth_jwt.public_key_path.read_text(),
    algorithms: str = settings.auth_jwt.algorithm,
):
    decoded = jwt.decode(token, public_key, algorithms)
    return decoded


def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(password=pwd_bytes, salt=salt)


def check_password(
    password: str,
    hashed_password: bytes,
) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password)
