from fastapi import FastAPI

from routers import auth, rooms, upload, chat

app = FastAPI(title="Multimodal RAG Platform — Education")

app.include_router(auth.router)
app.include_router(rooms.router)
app.include_router(upload.router)
app.include_router(chat.router)


@app.get("/")
def root():
    return {"status": "ok", "message": "Multimodal RAG Platform API running"}