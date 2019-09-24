"""Models for echo-controller"""
from datetime import datetime
from sqlalchemy import Integer, String, Column, DateTime, ForeignKey

from database import Base
from auth.models import User
from sqlalchemy.orm import relationship


class Message(Base):
    """
    Base model for users messages
    id - primary key, autoincrement
    relations with User from auth app
    """

    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(String, nullable=True)
    created = Column(DateTime, default=datetime.now())
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(User, back_populates='messages')
