from sqlalchemy import Table, Integer, String, Column, DateTime
from sqlalchemy.orm import mapper

from database import metadata

message_table = Table(
        'messages', metadata,
        Column('id', Integer, primary_key=True),
        Column('content', String),
        Column('user', String),
        Column('created', DateTime),
    )


class Message:
    def __init__(self, content, user, date):
        self.content = content
        self.user = user
        self.date = date


echo = mapper(Message, message_table)
