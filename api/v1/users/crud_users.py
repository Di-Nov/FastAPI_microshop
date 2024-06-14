from api.v1.users.schemas_users import CreateUser


def create_user(user_in: CreateUser) -> dict:
    user = user_in.model_dump()
    return {
        "success": True,
        "user": user
    }
