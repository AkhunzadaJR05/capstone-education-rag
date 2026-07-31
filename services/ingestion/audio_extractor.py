import os
os.environ["PATH"] += os.pathsep + r"C:\ffmpeg\bin"

import whisper

_whisper_model = None


def get_whisper_model():
    global _whisper_model
    if _whisper_model is None:
        _whisper_model = whisper.load_model("base")
    return _whisper_model


def extract_audio(file_path: str) -> list[str]:
    file_path = os.path.abspath(file_path)
    model = get_whisper_model()
    result = model.transcribe(file_path)
    text = result["text"]
    chunks = [chunk.strip() for chunk in text.split(". ") if chunk.strip()]
    return chunks