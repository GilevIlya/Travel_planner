from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.project import (
    ProjectCreate,
    ProjectListOut,
    ProjectOut,
    ProjectUpdate,
)
from app.services.project_service import ProjectService

router = APIRouter(prefix="/api/v1/projects", tags=["Projects"])


@router.post(
    "",
    response_model=ProjectOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a travel project",
    description="Create a new travel project. Optionally include an array of place names to add them in one request. Example: {\"name\": \"Europe Trip\", \"places\": [\"Eiffel Tower\", \"Colosseum\"]}",
)
async def create_project(data: ProjectCreate, db: AsyncSession = Depends(get_db)):
    service = ProjectService(db)
    project = await service.create_project(data)
    return project


@router.get(
    "",
    response_model=list[ProjectListOut],
    summary="List travel projects",
    description="Retrieve a paginated list of all travel projects. Supports pagination via `page` and `size` query parameters.",
)
async def list_projects(
    page: int = 1,
    size: int = 20,
    db: AsyncSession = Depends(get_db),
):
    service = ProjectService(db)
    projects, total = await service.list_projects(page=page, size=size)
    return [
        ProjectListOut(
            id=p.id,
            name=p.name,
            description=p.description,
            start_date=p.start_date,
            is_completed=p.is_completed,
            created_at=p.created_at,
            updated_at=p.updated_at,
            places_count=len(p.places),
        )
        for p in projects
    ]


@router.get(
    "/{project_id}",
    response_model=ProjectOut,
    summary="Get a travel project",
    description="Retrieve a single travel project by its ID, including all associated places.",
)
async def get_project(project_id: int, db: AsyncSession = Depends(get_db)):
    service = ProjectService(db)
    return await service.get_project(project_id)


@router.patch(
    "/{project_id}",
    response_model=ProjectOut,
    summary="Update a travel project",
    description="Update the name, description, and/or start date of an existing travel project. Only provided fields will be updated.",
)
async def update_project(
    project_id: int,
    data: ProjectUpdate,
    db: AsyncSession = Depends(get_db),
):
    service = ProjectService(db)
    return await service.update_project(project_id, data)


@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a travel project",
    description="Delete a travel project. Fails with 400 if any place in the project is already marked as visited.",
)
async def delete_project(project_id: int, db: AsyncSession = Depends(get_db)):
    service = ProjectService(db)
    await service.delete_project(project_id)