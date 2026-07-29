import os
import uuid

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from db.database import get_db
from db.models import ChatRoom, UploadedFile, User
from services.auth import get_current_user
from services.embedder import embed_texts
from services.vector_store import client, ensure_collection, COLLECTION_NAME
from services.ingestion.pdf import extract_pdf
from services.ingestion.docx_extractor import extract_docx
from services.ingestion.csv_extractor import extract_csv
from services.ingestion.text_extractor import extract_text_file
from services.ingestion.pptx_extractor import extract_pptx
from services.ingestion.image_extractor import extract_image
from services.ingestion.audio_extractor import extract_audio
from services.ingestion.video_extractor import extract_video
from qdrant_client.models import PointStruct

router = APIRouter(tags=["upload"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

EXTRACTORS = {
    ".pdf": extract_pdf,
    ".docx": extract_docx,
    ".csv": extract_csv,
    ".md": extract_text_file,
    ".txt": extract_text_file,
    ".pptx": extract_pptx,
    ".png": extract_image,
    ".jpg": extract_image,
    ".jpeg": extract_image,
    ".mp3": extract_audio,
    ".wav": extract_audio,
    ".m4a": extract_audio,
    ".mp4": extract_video,
    ".mov": extract_video,
}


@router.post("/upload/{room_id}")
def upload_file(
    room_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    room = db.query(ChatRoom).filter(ChatRoom.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    if room.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your room")

    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in EXTRACTORS:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {ext}")

    saved_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4()}{ext}")
    with open(saved_path, "wb") as f:
        f.write(file.file.read())

    db_file = UploadedFile(
        room_id=room_id,
        filename=file.filename,
        file_type=ext.lstrip("."),
        file_path=saved_path,
        status="processing",
    )
    db.add(db_file)
    db.commit()
    db.refresh(db_file)

    try:
        extractor = EXTRACTORS[ext]
        chunks = extractor(saved_path)

        if not chunks:
            raise ValueError("No text extracted from file")

        vectors = embed_texts(chunks)

        ensure_collection()
        points = [
            PointStruct(
                id=str(uuid.uuid4()),
                vector=vectors[i],
                payload={
                    "room_id": room_id,
                    "file_id": db_file.id,
                    "filename": file.filename,
                    "chunk_index": i,
                    "file_type": ext.lstrip("."),
                    "text": chunks[i],
                },
            )
            for i in range(len(chunks))
        ]
        client.upsert(collection_name=COLLECTION_NAME, points=points)

        db_file.status = "ready"
        db.commit()

        return {"file_id": db_file.id, "chunks_created": len(chunks), "status": "ready"}

    except Exception as e:
        db_file.status = "failed"
        db.commit()
        raise HTTPException(status_code=500, detail=f"Extraction failed: {str(e)}")