from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, CheckConstraint
from app.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)

class Movie(Base):
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    release_year = Column(Integer)
    created_at = Column(DateTime, nullable=False, default=datetime.now)

class List(Base):
    __tablename__ = 'lists'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)

class ListMember(Base):
    __tablename__ = 'list_members'
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    list_id = Column(Integer, ForeignKey("lists.id"), primary_key=True)

class ListMovie(Base):
    __tablename__ = 'list_movies'
    __table_args__ = (CheckConstraint("status in ('assistir', 'assistido', 'assistindo', 'largado')", name='check_status'),
                      CheckConstraint("rating between 1 and 10", name='check_rating'))
    movie_id = Column(Integer, ForeignKey("movies.id"), primary_key=True)
    list_id = Column(Integer, ForeignKey("lists.id"), primary_key=True)
    status = Column(String(50), nullable=False)
    rating = Column(Integer)
    notes = Column(String(255))
    created_at = Column(DateTime, nullable=False, default=datetime.now)
