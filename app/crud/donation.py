from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from sqlalchemy import select

from .base import CRUDBase
from models import Donation, User
from schemas.donation import DonationCreate


class CRUDDonation(CRUDBase[Donation, None, DonationCreate]):

    async def get_by_user(self, user: User, session: AsyncSession) -> Optional[List[Donation]]:
        donations_user = await session.execute(select(self.model).where(self.model.user_id == user.id))
        return donations_user.scalars().all()


donation_crud = CRUDDonation(Donation)
