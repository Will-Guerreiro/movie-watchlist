from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session
from app.models import List, ListMember
from app.schemas import ListCreate, ListResponse
from app.database import get_db
from app.auth import hash_password, verify_password, create_access_token, get_current_user

router = APIRouter()

@router.post("/lists", response_model=ListResponse)
def create_list(list_data: ListCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)) -> ListResponse:
    new_list_data = List(
        name = list_data.name,
        created_by = current_user.id
    )
    db.add(new_list_data)
    db.commit()
    db.refresh(new_list_data)
    return new_list_data

@router.get("/lists", response_model=list[ListResponse])
def get_lists(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    lists = (db.query(List).outerjoin(ListMember, List.id == ListMember.list_id)
             .where(or_(List.created_by == current_user.id, ListMember.user_id == current_user.id))
             .distinct()).all()
    return lists

@router.post("/lists/{list_id}/members")
def add_list_member(list_id : int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    search_list = db.query(List).where(List.id == list_id).first()
    if not search_list:
        raise HTTPException(status_code=404, detail="List not found")
    if not search_list.created_by == current_user.id:
        raise HTTPException(status_code=403, detail="User does not own list")
