from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from db.database import get_db
from db.models import ChatRoom, User
from services.auth import get_current_user

router = APIRouter(prefix="/rooms", tags=["rooms"])


class RoomCreateRequest(BaseModel):
    name: str
    description: str | None = None


class RoomResponse(BaseModel):
    id: int
    name: str
    description: str | None
    owner_id: int

    class Config:
        from_attributes = True


@router.get("", response_model=list[RoomResponse])
def list_rooms(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    return db.query(ChatRoom).filter(ChatRoom.owner_id == current_user.id).all()


@router.post("", response_model=RoomResponse, status_code=status.HTTP_201_CREATED)
def create_room(
    payload: RoomCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    room = ChatRoom(
        name=payload.name, description=payload.description, owner_id=current_user.id
    )
    db.add(room)
    db.commit()
    db.refresh(room)
    return room


@router.delete("/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_room(
    room_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    room = db.query(ChatRoom).filter(ChatRoom.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    if room.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your room")

    db.delete(room)
    db.commit()
    return None