from passlib.context import CryptContext
from repositories.user import UserRepository
from schemas.user import UserCreate, UserLogin, UserRead
from starlette.concurrency import run_in_threadpool


class UserService:
    def __init__(self, user_repo: UserRepository) -> None:
        self.user_repo = user_repo
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def register_user(self, user_in: UserCreate) -> UserRead:
        existing = await self.user_repo.get_by_username(user_in.username)

        if existing:
            raise ValueError("Username already exists")

        password_hash = await run_in_threadpool(
            self.pwd_context.hash,
            user_in.password,
        )

        user = await self.user_repo.create(user_in, password_hash)

        return UserRead.model_validate(user)

    async def authenticate_user(self, user_in: UserLogin) -> UserRead:
        user = await self.user_repo.get_by_username(user_in.username)

        if not user:
            raise ValueError("Invalid credentials")

        isValid = await run_in_threadpool(
            self.pwd_context.verify,
            user_in.password,
            user.password_hash,
        )

        if not isValid:
            raise ValueError("Invalid credentials")

        return UserRead.model_validate(user)
