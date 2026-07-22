from app.schemas import ChunkCreate
import tiktoken

from app.settings import settings


encoding = tiktoken.encoding_for_model(settings.EMBEDDING_MODEL)


def split_into_chunks(
    text: str,
    chunk_size: int = settings.CHUNK_SIZE,
    overlap: int = settings.CHUNK_OVERLAP,
) -> list[ChunkCreate]:
    chunks: list[ChunkCreate] = []

    step = chunk_size - overlap
    tokens = encoding.encode(text)

    for chunk_index, start in enumerate(range(0, len(tokens), step)):
        chunk_tokens = tokens[start:start + chunk_size]

        if not chunk_tokens:
            continue

        chunk_text = encoding.decode(chunk_tokens).strip()

        if not chunk_text:
            continue

        chunks.append(
            ChunkCreate(
                chunk_index=chunk_index,
                content=chunk_text,
            )
        )

    return chunks