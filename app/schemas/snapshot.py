from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class SnapshotCreate(BaseModel):
    tracked_page_id: int = Field(gt=0)
    content_hash: str = Field(min_length=64, max_length=64)
    content_text: str = Field(min_length=1)


class SnapshotRead(BaseModel):
    id: int
    tracked_page_id: int
    content_hash: str
    content_text: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
