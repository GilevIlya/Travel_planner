from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.project import TravelProject
from app.models.place import ProjectPlace


class ProjectRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, project: TravelProject) -> TravelProject:
        self.db.add(project)
        await self.db.flush()
        await self.db.refresh(project)
        return project

    async def get_by_id(self, project_id: int) -> TravelProject | None:
        stmt = (
            select(TravelProject)
            .options(selectinload(TravelProject.places))
            .where(TravelProject.id == project_id)
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_all(
        self, skip: int = 0, limit: int = 20
    ) -> list[TravelProject]:
        stmt = (
            select(TravelProject)
            .options(selectinload(TravelProject.places))
            .offset(skip)
            .limit(limit)
            .order_by(TravelProject.created_at.desc())
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def count_all(self) -> int:
        stmt = select(func.count(TravelProject.id))
        result = await self.db.execute(stmt)
        return result.scalar_one()

    async def update(self, project: TravelProject) -> TravelProject:
        self.db.add(project)
        await self.db.flush()
        await self.db.refresh(project)
        return project

    async def delete(self, project: TravelProject) -> None:
        await self.db.delete(project)
        await self.db.flush()