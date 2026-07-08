from datetime import date, datetime

from pydantic import BaseModel, Field


class ProjectPlaceOut(BaseModel):
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


class ProjectCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="Project name")
    description: str | None = Field(None, max_length=1000, description="Optional project description")
    start_date: date | None = Field(None, description="Optional start date (YYYY-MM-DD)")
    places: list[int] = Field(default=[], max_length=10, description="List of artwork external IDs from Art Institute Chicago API, e.g. [27992, 28563]")


class ProjectUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=255, description="Project name")
    description: str | None = Field(None, max_length=1000, description="Optional project description")
    start_date: date | None = Field(None, description="Optional start date (YYYY-MM-DD)")


class ProjectOut(BaseModel):
    id: int
    name: str
    description: str | None = None
    start_date: date | None = None
    is_completed: bool = False
    created_at: datetime
    updated_at: datetime
    places: list[ProjectPlaceOut] = []

    model_config = {"from_attributes": True}


class ProjectListOut(BaseModel):
    id: int
    name: str
    description: str | None = None
    start_date: date | None = None
    is_completed: bool = False
    created_at: datetime
    updated_at: datetime
    places_count: int = 0

    model_config = {"from_attributes": True}