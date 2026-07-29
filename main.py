from fastapi import FastAPI

from routers import auth, rooms, upload

app = FastAPI(title="Multimodal RAG Platform — Education")

app.include_router(auth.router)
app.include_router(rooms.router)
app.include_router(upload.router)


@app.get("/")
def root():
    return {"status": "ok", "message": "Multimodal RAG Platform API running"}