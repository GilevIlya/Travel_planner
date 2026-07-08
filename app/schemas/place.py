from datetime import datetime

from pydantic import BaseModel, Field


class PlaceCreate(BaseModel):
    external_id: int = Field(..., description="Artwork ID from Art Institute Chicago API, e.g. 27992")


class PlaceUpdate(BaseModel):
    notes: str | None = Field(None, max_length=5000, description="User notes for this place")
    is_visited: bool | None = Field(None, description="Mark place as visited")


class PlaceOut(BaseModel):
    id: int
    project_id: int
    external_id: int
    title: str
    artist_title: str | None = None
    image_id: str | None = None
    notes: str | None = None
    is_visited: bool = False
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}