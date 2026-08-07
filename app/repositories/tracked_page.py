from exceptions.traked_page import TrackedPageAlreadyExistsError
from models.tracked_page import TrackedPage
from schemas.tracked_page import TrackedPageCreate, TrackedPageUpdate
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession


class TrackedPageRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, page_id: int, user_id: int) -> TrackedPage | None:
        page = await self.session.execute(
            select(TrackedPage).where(TrackedPage.id == page_id, TrackedPage.user_id == user_id)
        )
        return page.scalar_one_or_none()

    async def get_all_by_user_id(self, user_id) -> list[TrackedPage]:
        pages = await self.session.execute(
            select(TrackedPage).where(TrackedPage.user_id == user_id)
        )
        return list(pages.scalars().all())

    async def create(self, user_id: int, page_in: TrackedPageCreate) -> TrackedPage:
        page = TrackedPage(user_id=user_id, url=page_in.url, status="active")
        self.session.add(page)
        try:
            await self.session.commit()
        except IntegrityError as e:
            raise TrackedPageAlreadyExistsError("You already track this URL") from e

        await self.session.refresh(page)
        return page

    async def update(self, page: TrackedPage, page_in: TrackedPageUpdate) -> TrackedPage:
        update_data = page_in.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(page, field, value)

        await self.session.commit()
        await self.session.refresh(page)
        return page

    async def delete(self, page: TrackedPage) -> None:
        await self.session.deleted(page)
        await self.session.commit()
