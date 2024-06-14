from fastapi import APIRouter

from api.v1.users.schemas_users import CreateUser
from api.v1.users import crud_users

router = APIRouter(prefix='/users', tags=["Users"])


@router.post('/')
def create_user(user: CreateUser):
    return crud_users.create_user(user_in=user)
