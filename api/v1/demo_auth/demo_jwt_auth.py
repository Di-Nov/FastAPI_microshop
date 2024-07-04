from fastapi import (
    APIRouter,
    Depends,
    Form,
    HTTPException,
    status,
)
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials,
    OAuth2PasswordBearer,
)
from pydantic import BaseModel
from jwt.exceptions import InvalidTokenError

from api.v1.users.schemas_users import UserSchema
from auth import utils as jwt_utils

router = APIRouter(
    prefix="/jwt",
    tags=["JWT"],
)

# http_bearer = HTTPBearer()
OAuth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/jwt/login/")


class TokenInfo(BaseModel):
    access_token: str
    token_type: str


john = UserSchema(
    username="John",
    password=jwt_utils.hash_password("qwerty"),
    email="john@example.com",
)

sam = UserSchema(
    username="Sam",
    password=jwt_utils.hash_password("privet"),
    email="Sam@example.com",
)


users_db: dict[str, UserSchema] = {
    john.username: john,
    sam.username: sam,
}


def validate_auth_user_login(
    username: str = Form(),
    password: str = Form(),
):
    unauthed_exeption = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid username or password",
    )

    if not (user := users_db.get(username)):
        raise unauthed_exeption

    elif not jwt_utils.check_password(password, user.password):
        raise unauthed_exeption

    elif not user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User in not active"
        )

    return user


@router.post("/login/", response_model=TokenInfo)
def auth_user_issue_jwt(user: UserSchema = Depends(validate_auth_user_login)):
    jwt_payload = {
        "sub": user.username,
        "username": user.username,
        "email": user.email,
    }
    token = jwt_utils.encode_jwt_token(payload=jwt_payload)
    return TokenInfo(access_token=token, token_type="Bearer")


def get_current_token_payload_user(
    # credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
    token: str = Depends(OAuth2_scheme),
):
    # token = credentials.credentials
    try:
        payload = jwt_utils.decode_jwt_token(
            token,
        )
    except InvalidTokenError as ex:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token error: {ex}",
        )

    return payload


def get_current_auth_user(
    payload: dict = Depends(get_current_token_payload_user),
):
    username: str | None = payload.get("sub")
    if user := users_db.get(username):
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token invalid (user not found)",
    )


def get_current_active_auth_user(user: UserSchema = Depends(get_current_auth_user)):
    if user.active:
        return user
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User inactive")


@router.get("/users/me/")
def auth_user_check_auth_info(
    payload: dict = Depends(get_current_token_payload_user),
    user: UserSchema = Depends(get_current_active_auth_user),
):
    iat: str = payload.get("iat")
    return {
        "username": user.username,
        "email": user.email,
        "logged_user": iat,
    }
