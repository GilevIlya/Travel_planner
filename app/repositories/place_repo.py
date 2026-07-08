from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.place import ProjectPlace


class PlaceRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, place: ProjectPlace) -> ProjectPlace:
        self.db.add(place)
        await self.db.flush()
        await self.db.refresh(place)
        return place

    async def get_by_id(self, place_id: int, project_id: int) -> ProjectPlace | None:
        stmt = (
            select(ProjectPlace)
            .where(ProjectPlace.id == place_id, ProjectPlace.project_id == project_id)
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_by_project(self, project_id: int, skip: int = 0, limit: int = 20) -> list[ProjectPlace]:
        stmt = (
            select(ProjectPlace)
            .where(ProjectPlace.project_id == project_id)
            .offset(skip)
            .limit(limit)
            .order_by(ProjectPlace.created_at.asc())
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def count_by_project(self, project_id: int) -> int:
        stmt = select(func.count(ProjectPlace.id)).where(ProjectPlace.project_id == project_id)
        result = await self.db.execute(stmt)
        return result.scalar_one()

    async def count_visited_by_project(self, project_id: int) -> int:
        stmt = select(func.count(ProjectPlace.id)).where(
            ProjectPlace.project_id == project_id,
            ProjectPlace.is_visited == True,
        )
        result = await self.db.execute(stmt)
        return result.scalar_one()

    async def find_by_external_id_and_project(self, external_id: int, project_id: int) -> ProjectPlace | None:
        stmt = select(ProjectPlace).where(
            ProjectPlace.external_id == external_id,
            ProjectPlace.project_id == project_id,
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def update(self, place: ProjectPlace) -> ProjectPlace:
        self.db.add(place)
        await self.db.flush()
        await self.db.refresh(place)
        return place

    async def delete(self, place: ProjectPlace) -> None:
        await self.db.delete(place)
        await self.db.flush()