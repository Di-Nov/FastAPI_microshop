import uuid
from time import time

from fastapi import APIRouter, Depends, HTTPException, status, Header, Response, Cookie
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from typing import Annotated, Any
import secrets


router = APIRouter(
    prefix="/demo-auth",
    tags=[
        "Demo Auth",
    ],
)

security = HTTPBasic()

USERNAME_TO_PASSWORD = {
    "admin": "admin",
    "user1": "qwerty",
}

STATIC_AUTH_TOKEN_TO_USERNAME = {
    "9afe85422044df1e8560c030dd2eee26": "admin",
    "b6f2196575390e9788d4b384229dd463": "user",
}

COOKIES: dict[str, dict[str, Any]] = {}
COOKIE_SESSION_ID_KEY = "web-app-session-cookie-id"


@router.get("/basic-auth/")
async def demo_basic_auth_credentials(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)]
):
    return {
        "massege": "Hi",
        "Name": credentials.username,
        "Password": credentials.password,
    }


def get_auth_username(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    exception_for_auth_user = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password",
    )
    correct_password = USERNAME_TO_PASSWORD.get(credentials.username)
    if correct_password is None:
        raise exception_for_auth_user
    elif not secrets.compare_digest(
        credentials.password.encode("utf-8"),
        correct_password.encode("utf-8"),
    ):
        raise exception_for_auth_user
    else:
        return credentials.username


@router.get("/basic-auth-username/")
async def demo_basic_auth_username(auth_username: str = Depends(get_auth_username)):
    return {
        "message": f"Hi {auth_username}",
        "Name": auth_username,
    }


def get_user_by_static_token(static_auth_token: str = Header(alias="x-auth-token")):
    if username := STATIC_AUTH_TOKEN_TO_USERNAME[static_auth_token]:
        return username

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token invalid",
    )


@router.get("/some-http-header-auth/")
async def demo_auth_some_http_header(
    auth_username: str = Depends(get_user_by_static_token),
):
    return {
        "message": f"Hi {auth_username}",
        "Name": auth_username,
    }


@router.post("/login-cookie/")
async def demo_auth_login_set_cookie(
    response: Response,
    # auth_username: str = Depends(get_auth_username),
    auth_username: str = Depends(get_user_by_static_token),
):
    session_id = uuid.uuid4().hex
    response.set_cookie(COOKIE_SESSION_ID_KEY, session_id)
    COOKIES[session_id] = {"username": auth_username, "time": int(time())}
    return {
        "result": "Ok",
    }


def get_session_id_data(session_id: str = Cookie(alias=COOKIE_SESSION_ID_KEY)):
    if session_id not in COOKIES:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not auth",
        )
    return COOKIES[session_id]


@router.get("/check_cookie/")
def demo_auth_check_cookie(user_session_data: dict = Depends(get_session_id_data)):
    return {**user_session_data}


@router.get("/logout-cookie/")
def demo_auth_logout_cookie(
    response: Response,
    session_id: str = Cookie(alias=COOKIE_SESSION_ID_KEY),
    user_session_data: dict = Depends(get_session_id_data),
):
    COOKIES.pop(session_id)
    response.delete_cookie(COOKIE_SESSION_ID_KEY)
    username = user_session_data["username"]
    return {"message": f"Bye, {username}"}
