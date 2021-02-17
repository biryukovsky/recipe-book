import datetime as dt

from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from flask_login import UserMixin

from recipe_book.db import Base


class User(UserMixin, Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, index=True)
    password = Column(String(100))

    recipes = relationship('Recipe', back_populates='user')


class Recipe(Base):
    __tablename__ = 'recipe'

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    slug = Column(String(50), unique=True, index=True, nullable=False)
    cooking_time = Column(String(30))
    instruction = Column(Text, nullable=False)
    created_at = Column(DateTime, default=dt.datetime.utcnow)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)

    ingredients = relationship('Ingredient', back_populates='recipe')
    user = relationship('User', back_populates='recipes')


class Ingredient(Base):
    __tablename__ = 'ingredient'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    amount = Column(String(100), nullable=False)
    recipe_id = Column(Integer, ForeignKey('recipe.id'), nullable=False)

    recipe = relationship('Recipe', back_populates='ingredients')
