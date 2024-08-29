from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.auth.exceptions import LoginException
from src.auth.schemas import RegistrationSchema, TokenSchema
from src.auth.dependencies import get_user_service
from src.auth.services import UserService, create_token, verify_password


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> TokenSchema:
    user = await user_service.get_by_username(form_data.username)
    if user is None:
        raise LoginException

    if not verify_password(form_data.password, user.hashed_password):
        raise LoginException

    token = create_token(user.username)

    return {"access_token": token}


@router.post("/register")
async def register(
    user_data: RegistrationSchema,
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> str:
    await user_service.create_user(user_data.username, user_data.password)
    return "Вы успешно зарегистрировались"
