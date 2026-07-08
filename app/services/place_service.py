from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import (
    ArtworkNotFoundError,
    DuplicatePlaceError,
    PlaceNotFoundError,
    ProjectNotFoundError,
    ProjectPlaceLimitError,
)
from app.models.place import ProjectPlace
from app.repositories.place_repo import PlaceRepository
from app.repositories.project_repo import ProjectRepository
from app.schemas.place import PlaceCreate, PlaceUpdate
from app.services.art_api import ArtInstituteAPI

MAX_PLACES_PER_PROJECT = 10


class PlaceService:
    def __init__(self, db: AsyncSession):
        self.place_repo = PlaceRepository(db)
        self.project_repo = ProjectRepository(db)

    async def add_place(self, project_id: int, data: PlaceCreate) -> ProjectPlace:
        project = await self.project_repo.get_by_id(project_id)
        if not project:
            raise ProjectNotFoundError(project_id)

        current_count = await self.place_repo.count_by_project(project_id)
        if current_count >= MAX_PLACES_PER_PROJECT:
            raise ProjectPlaceLimitError(project_id, MAX_PLACES_PER_PROJECT)

        existing = await self.place_repo.find_by_external_id_and_project(
            data.external_id, project_id
        )
        if existing:
            raise DuplicatePlaceError(str(data.external_id), project_id)

        # Fetch from Art Institute API
        artwork = await ArtInstituteAPI.get_artwork(data.external_id)
        if not artwork:
            raise ArtworkNotFoundError(data.external_id)

        place = ProjectPlace(
            project_id=project_id,
            external_id=artwork["external_id"],
            title=artwork["title"],
            artist_title=artwork.get("artist_title"),
            image_id=artwork.get("image_id"),
        )
        return await self.place_repo.create(place)

    async def get_place(self, project_id: int, place_id: int) -> ProjectPlace:
        project = await self.project_repo.get_by_id(project_id)
        if not project:
            raise ProjectNotFoundError(project_id)

        place = await self.place_repo.get_by_id(place_id, project_id)
        if not place:
            raise PlaceNotFoundError(place_id, project_id)
        return place

    async def list_places(
        self, project_id: int, page: int = 1, size: int = 20
    ) -> tuple[list[ProjectPlace], int]:
        project = await self.project_repo.get_by_id(project_id)
        if not project:
            raise ProjectNotFoundError(project_id)

        skip = (page - 1) * size
        places = await self.place_repo.list_by_project(project_id, skip=skip, limit=size)
        total = await self.place_repo.count_by_project(project_id)
        return places, total

    async def update_place(self, project_id: int, place_id: int, data: PlaceUpdate) -> ProjectPlace:
        project = await self.project_repo.get_by_id(project_id)
        if not project:
            raise ProjectNotFoundError(project_id)

        place = await self.place_repo.get_by_id(place_id, project_id)
        if not place:
            raise PlaceNotFoundError(place_id, project_id)

        if data.notes is not None:
            place.notes = data.notes
        if data.is_visited is not None:
            place.is_visited = data.is_visited

        place = await self.place_repo.update(place)

        # Check if all places are visited -> mark project as completed
        if place.is_visited:
            total_places = await self.place_repo.count_by_project(project_id)
            visited_places = await self.place_repo.count_visited_by_project(project_id)
            if total_places == visited_places:
                project.is_completed = True
                await self.project_repo.update(project)

        return place