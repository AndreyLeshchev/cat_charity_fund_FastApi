from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, PositiveInt, validator


class CharityProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: PositiveInt = Field(...)


class CharityProjectRead(CharityProjectBase):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True


class CharityProjectCreate(CharityProjectBase):
    pass


class CharityProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1)
    full_amount: Optional[PositiveInt] = Field(None)

    @validator('name', 'description', 'full_amount')
    def value_not_null(cls, value):
        if value is None:
            raise ValueError('Поле не может быть пустым')
        return value