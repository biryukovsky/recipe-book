from sqlalchemy import Column, Integer, String

from flask_login import UserMixin

from recipe_book.db import Base


class User(UserMixin, Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, index=True)
    password = Column(String(100))
