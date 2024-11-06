from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.donation import DonationRead, DonationCreate, DonationReadAll
from core.db import get_async_session
from crud.donation import donation_crud
from models import User, CharityProject
from core.user import current_user, current_superuser
from services.invest import invest

router = APIRouter()


@router.get(
    '/', response_model=List[DonationReadAll],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(session: AsyncSession = Depends(get_async_session)):
    """
    Только для суперюзеров.
    \n
    Возвращает список всех пожертвований.
    """
    donations = await donation_crud.get_multi(session)
    return donations


@router.post(
    '/', response_model=DonationRead,
    response_model_exclude_none=True,
)
async def create_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """Сделать пожертвование."""
    donation = await donation_crud.create(donation, session, user)
    await invest(donation, CharityProject, session)
    return donation


@router.get(
    '/my', response_model=List[DonationRead],
    response_model_exclude_none=True,
)
async def get_user_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """Вернуть список пожертвований пользователя, выполняющего запрос."""
    donations = await donation_crud.get_by_user(user, session)
    return donations