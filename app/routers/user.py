from typing import Annotated

from core.database import get_db_session
from fastapi import APIRouter, Depends, HTTPException, status
from repositories.user import UserRepository
from schemas.user import UserCreate, UserLogin, UserRead
from services.user import UserService
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/auth", tags=["auth"])


def create_user_service(session: AsyncSession) -> UserService:
    return UserService(UserRepository(session))


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(
    user_in: UserCreate, session: Annotated[AsyncSession, Depends(get_db_session)]
) -> UserRead:
    service = create_user_service(session)
    try:
        return await service.register_user(user_in)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e


@router.post("/login", response_model=UserRead)
async def login(
    user_in: UserLogin, session: Annotated[AsyncSession, Depends(get_db_session)]
) -> UserRead:
    service = create_user_service(session)
    try:
        return await service.authenticate_user(user_in)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e)) from e
