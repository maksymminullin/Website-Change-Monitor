from typing import Annotated

from core.database import get_db_session
from exceptions.snapshot import SnapshotNotFoundError
from exceptions.tracked_page import TrackedPageNotFoundError
from fastapi import APIRouter, Depends, HTTPException, status
from repositories.snapshot import SnapshotRepository
from repositories.tracked_page import TrackedPageRepository
from schemas.snapshot import SnapshotCreate, SnapshotRead
from services.snapshot import SnapshotService
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
    prefix="/snapshots",
    tags=["snapshots"],
)


def create_snapshot_service(
    session: AsyncSession,
) -> SnapshotService:
    return SnapshotService(
        snapshot_repo=SnapshotRepository(session),
        tracked_page_repo=TrackedPageRepository(session),
    )


@router.post("", response_model=SnapshotRead, status_code=status.HTTP_201_CREATED)
async def create_snapshot(
    snapshot_in: SnapshotCreate,
    user_id: int,
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> SnapshotRead:
    service = create_snapshot_service(session)

    try:
        return await service.create_snapshot(
            user_id=user_id,
            snapshot_in=snapshot_in,
        )

    except TrackedPageNotFoundError as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(err),
        ) from err


@router.get("/tracked-page/{tracked_page_id}", response_model=list[SnapshotRead])
async def get_all_snapshots(
    tracked_page_id: int, user_id: int, session: Annotated[AsyncSession, Depends(get_db_session)]
) -> list[SnapshotRead]:
    service = create_snapshot_service(session)

    try:
        return await service.get_all_snapshots(
            user_id=user_id,
            tracked_page_id=tracked_page_id,
        )

    except TrackedPageNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e


@router.get("/tracked-page/{tracked_page_id}/{snapshot_id}", response_model=SnapshotRead)
async def get_snapshot(
    tracked_page_id: int,
    snapshot_id: int,
    user_id: int,
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> SnapshotRead:
    service = create_snapshot_service(session)

    try:
        return await service.get_snapshot(
            user_id=user_id,
            tracked_page_id=tracked_page_id,
            snapshot_id=snapshot_id,
        )

    except TrackedPageNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e

    except SnapshotNotFoundError as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(err),
        ) from err


@router.delete(
    "/tracked-page/{tracked_page_id}/{snapshot_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_snapshot(
    tracked_page_id: int,
    snapshot_id: int,
    user_id: int,
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> None:
    service = create_snapshot_service(session)

    try:
        await service.delete_snapshot(
            user_id=user_id,
            tracked_page_id=tracked_page_id,
            snapshot_id=snapshot_id,
        )

    except TrackedPageNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e

    except SnapshotNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
