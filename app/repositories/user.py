from models.user import User
from schemas.user import UserCreate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_username(self, username: str) -> User | None:
        result = await self.session.execute(select(User).where(User.username == username))

        return result.scalar_one_or_none()

    async def create(self, user_id: UserCreate, password_hash: str) -> User:
        user = User(username=user_id.username, password_hash=password_hash)

        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user
