import pymupdf4llm


def extract_pdf(file_path: str) -> list[str]:
    text = pymupdf4llm.to_markdown(file_path)
    chunks = [chunk.strip() for chunk in text.split("\n\n") if chunk.strip()]
    return chunks