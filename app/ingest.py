from pathlib import Path

from app.chunking import split_into_chunks
from app.chunks_repository import save_chunks
from app.db import SessionLocal
from app.embeddings import embed_chunks
from app.pdf import extract_text
from app.schemas import ChunkCreate
from app.schemas import ChunkWithEmbedding


async def ingest(pdf_path: Path | str):
    pdf_path = Path(pdf_path)

    text: str = extract_text(pdf_path)
    chunks: list[ChunkCreate] = split_into_chunks(text)
    embedded_chunks: list[ChunkWithEmbedding] = await embed_chunks(chunks)

    async with SessionLocal() as session:
        await save_chunks(session, embedded_chunks, pdf_path.name)
