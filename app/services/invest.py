from datetime import datetime as dt
from typing import Union
from sqlalchemy.ext.asyncio import AsyncSession

from crud.base import CRUDBase
from models import CharityProject, Donation


async def close_invest(obj: Union[CharityProject, Donation]):
    obj.close_date = dt.now()
    obj.fully_invested = True
    obj.invested_amount = obj.full_amount
    return obj


async def invest(
    obj_in: Union[CharityProject, Donation],
    obj_from: Union[CharityProject, Donation],
    session: AsyncSession,
):
    all_invest = await CRUDBase(obj_from).get_all_invested(session)
    for invest in all_invest:
        investing = invest.full_amount - invest.invested_amount
        open_invest = obj_in.full_amount - obj_in.invested_amount
        if open_invest > investing:
            obj_in.invested_amount += investing
            await close_invest(invest)
            break
        if open_invest < investing:
            invest.invested_amount += open_invest
            await close_invest(obj_in)
            session.add(obj_in)
        if open_invest == investing:
            await close_invest(invest)
            await close_invest(obj_in)
            session.add(obj_in)
    session.add(invest)
    await session.commit()
    await session.refresh(obj_in)
    return obj_in