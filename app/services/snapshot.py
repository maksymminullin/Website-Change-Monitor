from exceptions.snapshot import SnapshotNotFoundError
from exceptions.tracked_page import TrackedPageNotFoundError
from repositories.snapshot import SnapshotRepository
from repositories.tracked_page import TrackedPageRepository
from schemas.snapshot import SnapshotCreate, SnapshotRead


class SnapshotService:
    def __init__(
        self, snapshot_repo: SnapshotRepository, tracked_page_repo: TrackedPageRepository
    ) -> None:
        self.snapshot_repo = snapshot_repo
        self.tracked_page_repo = tracked_page_repo

    async def create_snapshot(self, user_id: int, snapshot_in: SnapshotCreate) -> SnapshotRead:
        tracked_page = await self.tracked_page_repo.get_by_id(
            user_id=user_id, page_id=snapshot_in.tracked_page_id
        )
        if tracked_page is None:
            raise TrackedPageNotFoundError("Tracked page not found")

        snapshot = await self.snapshot_repo.create(snapshot_in=snapshot_in)

        return SnapshotRead.model_validate(snapshot)

    async def get_snapshot(
        self, user_id: int, tracked_page_id: int, snapshot_id: int
    ) -> SnapshotRead:
        tracked_page = await self.tracked_page_repo.get_by_id(
            user_id=user_id, page_id=tracked_page_id
        )
        if tracked_page is None:
            raise TrackedPageNotFoundError("Tracked page not found")

        snapshot = await self.snapshot_repo.get_by_id(
            snapshot_id=snapshot_id, tracked_page_id=tracked_page_id
        )
        if snapshot is None:
            raise SnapshotNotFoundError("Snapshot not found")

        return SnapshotRead.model_validate(snapshot)

    async def get_all_snapshots(self, user_id: int, tracked_page_id: int) -> list[SnapshotRead]:
        tracked_page = await self.tracked_page_repo.get_by_id(
            user_id=user_id, page_id=tracked_page_id
        )
        if tracked_page is None:
            raise TrackedPageNotFoundError("Tracked page not found")

        snapshots = await self.snapshot_repo.get_all_by_tracked_page_id(
            tracked_page_id=tracked_page_id
        )
        return [SnapshotRead.model_validate(snapshot) for snapshot in snapshots]

    async def delete_snapshot(self, user_id: int, tracked_page_id: int, snapshot_id: int) -> None:
        tracked_page = await self.tracked_page_repo.get_by_id(
            user_id=user_id, page_id=tracked_page_id
        )
        if tracked_page is None:
            raise TrackedPageNotFoundError("Tracked page not found")

        snapshot = await self.snapshot_repo.get_by_id(
            snapshot_id=snapshot_id, tracked_page_id=tracked_page_id
        )
        if snapshot is None:
            raise SnapshotNotFoundError("Snapshot not found")

        await self.snapshot_repo.delete(snapshot)
