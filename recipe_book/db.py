from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from recipe_book.config import Config


db_engine = create_engine(Config.DATABASE_URI)

Base = declarative_base(bind=db_engine)
