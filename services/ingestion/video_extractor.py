import subprocess
import tempfile
import os

from services.ingestion.audio_extractor import get_whisper_model


def extract_video(file_path: str) -> list[str]:
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        audio_path = tmp.name

    subprocess.run(
        ["ffmpeg", "-y", "-i", file_path, "-vn", "-acodec", "pcm_s16le", "-ar", "16000", audio_path],
        check=True,
        capture_output=True,
    )

    model = get_whisper_model()
    result = model.transcribe(audio_path)
    text = result["text"]

    os.remove(audio_path)

    chunks = [chunk.strip() for chunk in text.split(". ") if chunk.strip()]
    return chunks