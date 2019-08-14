from sqlalchemy import (
    create_engine, Table, String, Integer, DateTime, MetaData, Column
)
from sqlalchemy.orm import mapper
from models import Client, ClientHistory, Contacts


def migrate():
    engine = create_engine('sqlite:///data.db')
    metadata = MetaData()

    client_table = Table(
        'clients', metadata,
        Column('id', Integer, primary_key=True),
        Column('login', String),
        Column('information', String),
    )

    client_history_table = Table(
        'client_histories', metadata,
        Column('id', Integer, primary_key=True),
        Column('enter_time', DateTime),
        Column('ip_address', String),
    )

    contacts_table = Table(
        'contacts', metadata,
        Column('id', Integer, primary_key=True),
        Column('id_owner', String),
        Column('id_client', String),
    )

    metadata.create_all(engine)

    mapper(Client, client_table)
    mapper(ClientHistory, client_history_table)
    mapper(Contacts, contacts_table)


migrate()
