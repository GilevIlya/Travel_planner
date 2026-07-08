from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.place import PlaceCreate, PlaceOut, PlaceUpdate
from app.services.place_service import PlaceService

router = APIRouter(prefix="/api/v1/projects/{project_id}/places", tags=["Places"])


@router.post(
    "",
    response_model=PlaceOut,
    status_code=status.HTTP_201_CREATED,
    summary="Add an artwork to a project",
    description="Add a place to an existing travel project by providing an artwork ID from the Art Institute Chicago API. "
                "Validates that the artwork exists in the API, the place is not a duplicate, and the project has fewer than 10 places.",
)
async def add_place(
    project_id: int,
    data: PlaceCreate,
    db: AsyncSession = Depends(get_db),
):
    service = PlaceService(db)
    return await service.add_place(project_id, data)


@router.get(
    "",
    response_model=list[PlaceOut],
    summary="List places in a project",
    description="Retrieve a paginated list of all places in a travel project. Supports pagination via `page` and `size` query parameters.",
)
async def list_places(
    project_id: int,
    page: int = 1,
    size: int = 20,
    db: AsyncSession = Depends(get_db),
):
    service = PlaceService(db)
    places, total = await service.list_places(project_id, page=page, size=size)
    return places


@router.get(
    "/{place_id}",
    response_model=PlaceOut,
    summary="Get a place in a project",
    description="Retrieve a single place by its ID within a specific project.",
)
async def get_place(
    project_id: int,
    place_id: int,
    db: AsyncSession = Depends(get_db),
):
    service = PlaceService(db)
    return await service.get_place(project_id, place_id)


@router.patch(
    "/{place_id}",
    response_model=PlaceOut,
    summary="Update a place in a project",
    description="Update the notes and/or mark a place as visited. "
                "When all places in a project are marked as visited, the project is automatically marked as completed.",
)
async def update_place(
    project_id: int,
    place_id: int,
    data: PlaceUpdate,
    db: AsyncSession = Depends(get_db),
):
    service = PlaceService(db)
    return await service.update_place(project_id, place_id, data)