from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from db.database import get_db
from db.models import ChatRoom, ChatMessage, User
from services.auth import get_current_user
from services.embedder import embed_texts
from services.vector_store import search_chunks
from services.rag import generate_answer

router = APIRouter(tags=["chat"])


class ChatRequest(BaseModel):
    query: str


class Source(BaseModel):
    filename: str
    file_type: str
    chunk_index: int
    excerpt: str


class ChatResponse(BaseModel):
    answer: str
    sources: list[Source]


def check_room_access(room_id: int, current_user: User, db: Session) -> ChatRoom:
    room = db.query(ChatRoom).filter(ChatRoom.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    if room.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your room")
    return room


@router.post("/chat/{room_id}", response_model=ChatResponse)
def chat(
    room_id: int,
    payload: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    check_room_access(room_id, current_user, db)

    query_vector = embed_texts([payload.query])[0]
    retrieved_chunks = search_chunks(query_vector, room_id, top_k=5)

    past_messages = (
        db.query(ChatMessage)
        .filter(ChatMessage.room_id == room_id)
        .order_by(ChatMessage.created_at.desc())
        .limit(6)
        .all()
    )
    history = [{"role": m.role, "content": m.content} for m in reversed(past_messages)]

    if not retrieved_chunks:
        answer = "I don't know."
        sources = []
    else:
        answer = generate_answer(payload.query, retrieved_chunks, history)
        sources = [
            {
                "filename": c["filename"],
                "file_type": c["file_type"],
                "chunk_index": c["chunk_index"],
                "excerpt": c["text"][:150],
            }
            for c in retrieved_chunks
        ]

    user_msg = ChatMessage(room_id=room_id, user_id=current_user.id, role="user", content=payload.query)
    assistant_msg = ChatMessage(
        room_id=room_id, user_id=current_user.id, role="assistant", content=answer, sources=sources
    )
    db.add(user_msg)
    db.add(assistant_msg)
    db.commit()

    return {"answer": answer, "sources": sources}


@router.get("/chat/{room_id}/history")
def get_history(
    room_id: int,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    check_room_access(room_id, current_user, db)
    messages = (
        db.query(ChatMessage)
        .filter(ChatMessage.room_id == room_id)
        .order_by(ChatMessage.created_at)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return [
        {
            "id": m.id,
            "role": m.role,
            "content": m.content,
            "sources": m.sources,
            "created_at": m.created_at,
        }
        for m in messages
    ]


@router.delete("/chat/{room_id}/history")
def delete_history(
    room_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    check_room_access(room_id, current_user, db)
    db.query(ChatMessage).filter(ChatMessage.room_id == room_id).delete()
    db.commit()
    return {"status": "cleared"}