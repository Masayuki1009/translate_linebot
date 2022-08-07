from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URI = "sqlite:///fast_todo.db"

engine = create_engine(SQLALCHEMY_DATABASE_URI, future=True)
make_session = sessionmaker(bind=engine, future=True)
