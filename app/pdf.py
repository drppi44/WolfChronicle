import pymupdf
from pathlib import Path


def extract_text(path: Path | str) -> str:
    pages = []

    doc = pymupdf.open(path)

    for page in doc:
        pages.append(page.get_text())

    return '\n'.join(pages)