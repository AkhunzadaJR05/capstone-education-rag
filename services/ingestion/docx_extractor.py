import docx


def extract_docx(file_path: str) -> list[str]:
    document = docx.Document(file_path)
    chunks = [para.text.strip() for para in document.paragraphs if para.text.strip()]
    return chunks