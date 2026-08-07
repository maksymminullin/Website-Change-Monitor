from exceptions.traked_page import (
    EmptyTrackedPageUpdateError,
    TrackedPageNotFoundError,
)
from repositories.tracked_page import TrackedPageRepository
from schemas.tracked_page import TrackedPageCreate, TrackedPageRead, TrackedPageUpdate


class TrackedPageService:
    def __init__(self, repository: TrackedPageRepository) -> None:
        self.repository = repository

    async def get_all(self, user_id: int) -> list[TrackedPageRead]:
        pages = await self.repository.get_all_by_user_id(user_id=user_id)
        return [TrackedPageRead.model_validate(page) for page in pages]

    async def create(self, user_id: int, page_in: TrackedPageCreate) -> TrackedPageRead:
        try:
            page = await self.repository.create(user_id=user_id, page_in=page_in)
        except ValueError as e:
            raise TrackedPageNotFoundError("Tracked page not found") from e
        return TrackedPageRead.model_validate(page)

    async def delete(self, user_id: int, page_id: int) -> None:
        page = await self.repository.get_by_id(user_id=user_id, page_id=page_id)
        if page is None:
            raise TrackedPageNotFoundError("Tracked page not found")
        await self.repository.delete(page)

    async def update(
        self, user_id: int, page_id: int, page_in: TrackedPageUpdate
    ) -> TrackedPageRead:
        page = await self.repository.get_by_id(user_id=user_id, page_id=page_id)

        if page is None:
            raise TrackedPageNotFoundError("Tracked page not found")

        if not page_in.model_dump(exclude_unset=True):
            raise EmptyTrackedPageUpdateError("At least one field is required")

        updated_page = await self.repository.update(
            page=page,
            page_in=page_in,
        )
        return TrackedPageRead.model_validate(updated_page)
