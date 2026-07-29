def extract_text_file(file_path: str) -> list[str]:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    chunks = [chunk.strip() for chunk in content.split("\n\n") if chunk.strip()]
    return chunks