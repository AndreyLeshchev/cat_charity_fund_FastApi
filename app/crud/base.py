from typing import Optional, TypeVar, Generic, Type, List
from sqlalchemy import select, desc
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from models import User
from core.db import Base


ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):

    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(self, obj_id: int, session: AsyncSession) -> Optional[ModelType]:
        db_obj = await session.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        return db_obj.scalars().first()

    async def get_multi(self, session: AsyncSession) -> List[ModelType]:
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(self, obj_in: CreateSchemaType, session: AsyncSession, user: Optional[User] = None):
        obj_in_data = obj_in.dict()
        if user is not None:
            obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def get_all_invested(
        self,
        session: AsyncSession,
    ):
        invested = await session.execute(
            select(self.model).where(
                self.model.fully_invested == 0
            ).order_by(desc('create_date'))
        )
        return invested.scalars().all()
