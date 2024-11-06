from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select

from .base import CRUDBase
from models import CharityProject
from schemas.charityproject import CharityProjectUpdate, CharityProjectCreate


class CRUDCharityProject(CRUDBase[CharityProject, CharityProjectCreate, CharityProjectUpdate]):

    async def update(
        self, db_obj: CharityProject, obj_in: CharityProjectUpdate, session: AsyncSession,
    ) -> CharityProject:
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(self, db_obj: CharityProject, session: AsyncSession) -> CharityProject:
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    async def get_id_by_name(self, obj_name: str, session: AsyncSession) -> CharityProject:
        project = await session.execute(select(self.model).where(self.model.name == obj_name))
        return project.scalars().first()


charityproject_crud = CRUDCharityProject(CharityProject)