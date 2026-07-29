import pandas as pd


def extract_csv(file_path: str) -> list[str]:
    df = pd.read_csv(file_path)
    chunks = []
    for i, row in df.iterrows():
        row_text = ", ".join(f"{col}: {row[col]}" for col in df.columns)
        chunks.append(row_text)
    return chunks