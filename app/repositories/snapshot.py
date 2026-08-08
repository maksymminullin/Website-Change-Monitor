from models.snapshot import Snapshot
from schemas.snapshot import SnapshotCreate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class SnapshotRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, snapshot_id: int, tracked_page_id: int) -> Snapshot | None:
        snapshot = await self.session.execute(
            select(Snapshot).where(
                Snapshot.id == snapshot_id, Snapshot.tracked_page_id == tracked_page_id
            )
        )
        return snapshot.scalar_one_or_none()

    async def get_all_by_tracked_page_id(self, tracked_page_id: int) -> list[Snapshot]:
        snapshots = await self.session.execute(
            select(Snapshot)
            .where(Snapshot.tracked_page_id == tracked_page_id)
            .order_by(Snapshot.created_at.desc())
        )

        return list(snapshots.scalars().all())

    async def create(self, snapshot_in: SnapshotCreate) -> Snapshot:
        snapshot = Snapshot(
            tracked_page_id=snapshot_in.tracked_page_id,
            content_hash=snapshot_in.content_hash,
            content_text=snapshot_in.content_text,
        )

        self.session.add(snapshot)

        await self.session.commit()
        await self.session.refresh(snapshot)

        return snapshot

    async def delete(self, snapshot: Snapshot) -> None:
        await self.session.delete(snapshot)
        await self.session.commit()
