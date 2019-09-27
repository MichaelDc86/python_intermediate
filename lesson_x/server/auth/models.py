from datetime import datetime

from database import Base
from sqlalchemy import Column, Integer, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_imageattach.entity import Image, image_attachment


class UserPicture(Base, Image):
    """User's profile picture."""

    __tablename__ = 'user_picture'

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    user = relationship('User')


class User(Base):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    image = image_attachment('UserPicture')
    sessions = relationship('Session', back_populates='user')
    messages = relationship('Message', back_populates='user')


class Session(Base):

    __tablename__ = 'sessions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    token = Column(String, nullable=False, unique=True)
    created = Column(DateTime, default=datetime.now())
    closed = Column(DateTime, nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(User, back_populates='sessions')
