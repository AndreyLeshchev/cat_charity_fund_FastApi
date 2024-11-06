from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder

from crud.charityproject import charityproject_crud
from schemas.charityproject import CharityProjectUpdate
from models.charityproject import CharityProject


async def check_name_duplicate(project_name: str, session: AsyncSession):
    project = await charityproject_crud.get_id_by_name(project_name, session)
    if project is not None:
        raise HTTPException(status_code=400, detail='Проект с таким именем уже существует!')


async def check_delete_project(project: CharityProject):
    if project.invested_amount:
        raise HTTPException(status_code=400, detail='В проект были внесены средства, не подлежит удалению!')


async def check_update_project(db_obj: CharityProject, obj_in: CharityProjectUpdate, session: AsyncSession):
    obj_data = jsonable_encoder(db_obj)
    update_data = obj_in.dict(exclude_unset=True)
    if update_data.get('full_amount') is not None:
        if obj_data['full_amount'] > update_data['full_amount']:
            raise HTTPException(status_code=400, detail='Нелья установить значение full_amount меньше уже вложенной суммы.')