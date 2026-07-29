import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def extract_image(file_path: str) -> list[str]:
    image = Image.open(file_path)
    text = pytesseract.image_to_string(image)
    chunks = [chunk.strip() for chunk in text.split("\n\n") if chunk.strip()]
    if not chunks and text.strip():
        chunks = [text.strip()]
    return chunks