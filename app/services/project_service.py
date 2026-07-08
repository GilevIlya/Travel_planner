from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import (
    ArtworkNotFoundError,
    DuplicatePlaceError,
    ProjectHasVisitedPlacesError,
    ProjectNotFoundError,
)
from app.models.project import TravelProject
from app.models.place import ProjectPlace
from app.repositories.place_repo import PlaceRepository
from app.repositories.project_repo import ProjectRepository
from app.schemas.project import ProjectCreate, ProjectUpdate
from app.services.art_api import ArtInstituteAPI


class ProjectService:
    def __init__(self, db: AsyncSession):
        self.project_repo = ProjectRepository(db)
        self.place_repo = PlaceRepository(db)

    async def create_project(self, data: ProjectCreate) -> TravelProject:
        project = TravelProject(
            name=data.name,
            description=data.description,
            start_date=data.start_date,
        )
        project = await self.project_repo.create(project)

        for external_id in data.places:
            # Check duplicate
            existing = await self.place_repo.find_by_external_id_and_project(
                external_id, project.id
            )
            if existing:
                raise DuplicatePlaceError(str(external_id), project.id)

            # Fetch from Art Institute API
            artwork = await ArtInstituteAPI.get_artwork(external_id)
            if not artwork:
                raise ArtworkNotFoundError(external_id)

            place = ProjectPlace(
                project_id=project.id,
                external_id=artwork["external_id"],
                title=artwork["title"],
                artist_title=artwork.get("artist_title"),
                image_id=artwork.get("image_id"),
            )
            await self.place_repo.create(place)

        # reload with places
        return await self.project_repo.get_by_id(project.id)

    async def get_project(self, project_id: int) -> TravelProject:
        project = await self.project_repo.get_by_id(project_id)
        if not project:
            raise ProjectNotFoundError(project_id)
        return project

    async def list_projects(self, page: int = 1, size: int = 20) -> tuple[list[TravelProject], int]:
        skip = (page - 1) * size
        projects = await self.project_repo.list_all(skip=skip, limit=size)
        total = await self.project_repo.count_all()
        return projects, total

    async def update_project(self, project_id: int, data: ProjectUpdate) -> TravelProject:
        project = await self.project_repo.get_by_id(project_id)
        if not project:
            raise ProjectNotFoundError(project_id)

        if data.name is not None:
            project.name = data.name
        if data.description is not None:
            project.description = data.description
        if data.start_date is not None:
            project.start_date = data.start_date

        return await self.project_repo.update(project)

    async def delete_project(self, project_id: int) -> None:
        project = await self.project_repo.get_by_id(project_id)
        if not project:
            raise ProjectNotFoundError(project_id)

        visited_count = await self.place_repo.count_visited_by_project(project_id)
        if visited_count > 0:
            raise ProjectHasVisitedPlacesError(project_id)

        await self.project_repo.delete(project)