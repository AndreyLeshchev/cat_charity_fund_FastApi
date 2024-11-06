from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import get_async_session
from services.invest import invest
from schemas.charityproject import CharityProjectRead, CharityProjectCreate, CharityProjectUpdate
from crud.charityproject import charityproject_crud
from models import Donation
from core.user import current_superuser
from ..validators import check_name_duplicate, check_delete_project, check_update_project


router = APIRouter()


@router.get(
    '/', response_model=List[CharityProjectRead],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
):
    """Возвращает список всех проектов."""
    projects = await charityproject_crud.get_multi(session)
    return projects


@router.post(
    '/', response_model=CharityProjectRead,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_charity_project(
    project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Только для суперюзеров.
    \n
    Создаёт благотворительный проект.
    """
    await check_name_duplicate(project.name, session)
    new_project = await charityproject_crud.create(project, session)
    await invest(new_project, Donation, session)
    return new_project


@router.patch(
    '/{project_id}', response_model=CharityProjectRead,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def update_charity_project(
    project_id: int, obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Только для суперюзеров.
    \n
    Закрытый проект нельзя редактировать; нельзя установить требуемую сумму меньше уже вложенной.
    """
    db_obj = await charityproject_crud.get(project_id, session)
    await check_update_project(db_obj, obj_in, session)
    update_obj = await charityproject_crud.update(db_obj, obj_in, session)
    return update_obj


@router.delete(
    '/{project_id}', response_model=CharityProjectRead,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def delete_charity_project(
    project_id: int, session: AsyncSession = Depends(get_async_session),
):
    """
    Только для суперюзеров.
    \n
    Удаляет проект. Нельзя удалить проект, в который уже были инвестированы средства, его можно только закрыть.
    """
    project = await charityproject_crud.get(project_id, session)
    await check_delete_project(project)
    project = await charityproject_crud.remove(project, session)
    return project