import os
import re
from typing import List, Dict

def normalize_text(text: str) -> str:
    text = text.replace("\r\n", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()

def split_into_units(text: str) -> List[str]:
    units = []
    paragraphs = re.split(r"\n\s*\n", text)

    for paragraph in paragraphs:
        paragraph = paragraph.strip()

        if not paragraph:
            continue

        sentences = re.split(r"(?<=[.!?])\s+", paragraph)

        for sentence in sentences:
            sentence = sentence.strip()

            if sentence:
                units.append(sentence)

    return units



def chunk_text(text: str, chunk_size: int = 500, overlap_units: int = 1) -> List[str]:

    if chunk_size <= 0:
        raise ValueError("chunk size must be greater than zero")

    if overlap_units < 0:
        raise ValueError("overlap should be greater than or equal to zero")

    units = split_into_units(text)
    chunks = []
    current_units = []
    current_length = 0

    for unit in units:
        unit_length = len(units)
        if(current_units and current_length + unit_length + 1 > chunk_size):
            chunks.append(" ".join(current_units))

            if overlap_units > 0:
                current_units = current_units[-overlap_units:]
                current_length = sum(len(item) for item in current_units)

            else:
                current_units = []
                current_length = 0

        current_units.append(unit)
        current_length += unit_length + 1

    if current_units:
        chunks.append(" ".join(current_units))

    return chunks



def load_documents() -> List[Dict]:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    docs_dir = os.path.join(base_dir, "..", "data", "documents")

    chunked_docs = []

    if not os.path.exists(docs_dir):
        raise FileNotFoundError(f"WARNING: document directory not found at {docs_dir}")

    for file_name in sorted(os.listdir(docs_dir)):

        if not file_name.lower().endswith(".txt"):
            continue

        file_path = os.path.join(docs_dir, file_name)
        with open(file_path, "r", encoding="utf-8") as file:
            full_text = file.read()
            full_text = normalize_text(full_text)

            if not full_text:
                continue

            document_id = os.path.splitext(file_name)[0]

            text_chunks = chunk_text(full_text, chunk_size=300, overlap_units=50)

            for index, chunk_content in enumerate(text_chunks):
                chunked_docs.append({
                    "chunk_id": f"{document_id}_chunk_{index}",
                    "document_id": document_id,
                    "content": chunk_content,
                    "metadata": {
                        "source": file_name,
                        "chunk_index": index,
                        "document_type": "text"
                    }
                })


    return chunked_docs

if __name__ == "__main__":
    documents = load_documents()
    print(f"Loaded {len(documents)} chunks")
    print("\n-----------------------------")
    for document in documents:
        print("Chunk ID:", document["chunk_id"])

        print(
            "Source:", document["metadata"]["source"])

        print(
            "Content:", document["content"])
