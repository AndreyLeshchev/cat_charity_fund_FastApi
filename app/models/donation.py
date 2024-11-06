from sqlalchemy import Column, Integer, ForeignKey, Text

from .base import AbstractModel


class Donation(AbstractModel):
    user_id = Column(Integer, ForeignKey('user.id', name='fk_donation_user_id_user'))
    comment = Column(Text, nullable=True)