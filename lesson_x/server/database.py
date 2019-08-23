from sqlalchemy import create_engine, MetaData

engine = create_engine('sqlite:///data.db')
metadata = MetaData()
