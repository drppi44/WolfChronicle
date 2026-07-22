from sqlalchemy import desc
from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.embeddings import create_embedding
from app.models import Chunk
from app.schemas import ChunkWithEmbedding
from app.settings import settings


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


async def search_semantic(
    session: AsyncSession,
    query: str,
    limit: int,
) -> list[Chunk]:
    query_embedding = await create_embedding(query)

    stmt = (
        select(Chunk)
        .order_by(Chunk.embedding.cosine_distance(query_embedding))
        .limit(limit)
    )

    result = await session.execute(stmt)

    return list(result.scalars().all())


async def search_lexical(
    session: AsyncSession,
    query: str,
    limit: int,
) -> list[Chunk]:
    ts_query = func.plainto_tsquery("english", query)

    stmt = (
        select(Chunk)
        .where(Chunk.search_vector.op("@@")(ts_query))
        .order_by(
            desc(
                func.ts_rank(
                    Chunk.search_vector,
                    ts_query,
                )
            )
        )
        .limit(limit)
    )

    result = await session.scalars(stmt)
    return list(result)


def fuse_results(
        semantic_chunks: list[Chunk],
        lexical_chunks: list[Chunk],
        limit: int,
) -> list[Chunk]:
    scores: dict[int, float] = {}
    chunks_by_id: dict[int, Chunk] = {}

    for rank, chunk in enumerate(semantic_chunks, start=1):
        chunks_by_id[chunk.id] = chunk
        scores[chunk.id] = scores.get(chunk.id, 0.0) + 1 / (settings.RRF_K + rank)

    for rank, chunk in enumerate(lexical_chunks, start=1):
        chunks_by_id[chunk.id] = chunk
        scores[chunk.id] = scores.get(chunk.id, 0.0) + 1 / (settings.RRF_K + rank)

    sorted_ids = sorted(
        scores,
        key=lambda chunk_id: scores[chunk_id],
        reverse=True,
    )

    return [
        chunks_by_id[chunk_id]
        for chunk_id in sorted_ids[:limit]
    ]


async def search_hybrid(
    session: AsyncSession,
    query: str,
    limit: int = 10,
) -> list[Chunk]:
    semantic_chunks = await search_semantic(session, query, limit)
    lexical_chunks = await search_lexical(session, query, limit)

    return fuse_results(
        semantic_chunks,
        lexical_chunks,
        limit,
    )