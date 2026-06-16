from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import Movie, User
from app.schemas import MovieCreate, MovieResponse
from app.database import get_db
from app.auth import get_current_user

router = APIRouter()

@router.post("/movies", response_model=MovieResponse)
def create_movie(movie: MovieCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    existing_movie = db.query(Movie).where(Movie.title == movie.title,
                                           Movie.release_year == movie.release_year).first()
    if existing_movie:
        raise HTTPException(status_code=409, detail="Movie already exists")

    new_movie = Movie(
        title=movie.title,
        release_year=movie.release_year,
    )
    db.add(new_movie)
    db.commit()
    db.refresh(new_movie)
    return new_movie