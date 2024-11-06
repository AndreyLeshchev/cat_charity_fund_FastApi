from datetime import datetime
from typing import Optional

from pydantic import BaseModel, PositiveInt, NonNegativeInt


class DonationBase(BaseModel):
    full_amount: PositiveInt
    comment: Optional[str]


class DonationRead(DonationBase):
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationReadAll(DonationRead):
    user_id: int
    invested_amount: NonNegativeInt
    fully_invested: bool
    close_date: Optional[datetime]


class DonationCreate(DonationBase):
    pass