from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

from recipe_book.config import Config

DB_URL = 'sqlite:///db.sqlite'

db_engine = create_engine(Config.DATABASE_URI)
db_session = scoped_session(sessionmaker(autoflush=False,
                                         autocommit=False,
                                         bind=db_engine))

Base = declarative_base(bind=db_engine)
