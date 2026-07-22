from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.embeddings import create_embedding
from app.models import Chunk
from app.schemas import ChunkWithEmbedding


async def save_chunks(
    session: AsyncSession,
    chunks: list[ChunkWithEmbedding],
    source: str,
) -> None:
    db_chunks = [
        Chunk(
            source=source,
            chunk_index=chunk.chunk_index,
            content=chunk.content,
            embedding=chunk.embedding,
        )
        for chunk in chunks
    ]

    session.add_all(db_chunks)

    await session.commit()


async def search_chunks(
    session: AsyncSession,
    query: str,
    limit: int = 5,
) -> list[Chunk]:
    query_embedding = await create_embedding(query)

    stmt = (
        select(Chunk)
        .order_by(Chunk.embedding.cosine_distance(query_embedding))
        .limit(limit)
    )

    result = await session.execute(stmt)

    return list(result.scalars().all())