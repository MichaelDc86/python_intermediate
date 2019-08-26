from datetime import datetime

from database import Base
from sqlalchemy import Column, Integer, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship


class User(Base):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    sessions = relationship('Session', back_populates='user')
    messages = relationship('Message', back_populates='user')


class Session(Base):

    __tablename__ = 'sessions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    created = Column(DateTime, default=datetime.now())
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(User, back_populates='sessions')
