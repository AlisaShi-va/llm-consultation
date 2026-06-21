# Эндпоинты Auth Service
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.usecases.auth import AuthUsecase
from app.api.deps import get_auth_uc, get_current_user_id
from app.schemas.auth import RegisterRequest, TokenResponse
from app.schemas.user import UserPublic

router= APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserPublic, status_code=201)
async def register(
    payload: RegisterRequest,
    auth_uc: AuthUsecase = Depends(get_auth_uc)
):
    """Регистрация нового аккаунта"""
    return await auth_uc.register(payload)

@router.post("/login", response_model=TokenResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_uc: AuthUsecase = Depends(get_auth_uc)
):
    """Вход в систему (username = email)"""
    return await auth_uc.login(form_data.username, form_data.password)

@router.get("/me", response_model=UserPublic)
async def me(
    current_user_id: int = Depends(get_current_user_id),
    auth_uc: AuthUsecase = Depends(get_auth_uc)
):
    """Получение данных текущего авторизованного пользователя"""
    return await auth_uc.me(current_user_id)