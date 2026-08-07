from exceptions.user import InvalidCredentialsError, UserAlreadyExistsError
from passlib.context import CryptContext
from repositories.user import UserRepository
from schemas.user import UserCreate, UserLogin, UserRead
from starlette.concurrency import run_in_threadpool


class UserService:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def register(self, user_in: UserCreate) -> UserRead:
        existing = await self.repository.get_by_username(user_in.username)

        if existing:
            raise UserAlreadyExistsError("Username already exists")

        password_hash = await run_in_threadpool(
            self.pwd_context.hash,
            user_in.password,
        )

        user = await self.repository.create(user_in, password_hash)

        return UserRead.model_validate(user)

    async def authenticate(self, user_in: UserLogin) -> UserRead:
        user = await self.repository.get_by_username(user_in.username)

        if not user:
            raise InvalidCredentialsError("Invalid credentials")

        isValid = await run_in_threadpool(
            self.pwd_context.verify,
            user_in.password,
            user.password_hash,
        )

        if not isValid:
            raise InvalidCredentialsError("Invalid credentials")

        return UserRead.model_validate(user)
