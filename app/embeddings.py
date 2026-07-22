from openai import AsyncOpenAI

from app.schemas import ChunkCreate
from app.schemas import ChunkWithEmbedding
from app.settings import settings

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)


async def create_embedding(text: str) -> list[float]:
    response = await client.embeddings.create(
        model=settings.EMBEDDING_MODEL,
        input=text,
    )

    return response.data[0].embedding


async def create_embeddings(texts: list[str]) -> list[list[float]]:
    response = await client.embeddings.create(
        model=settings.EMBEDDING_MODEL,
        input=texts,
    )

    return [item.embedding for item in response.data]


async def embed_chunks(chunks: list[ChunkCreate]) -> list[ChunkWithEmbedding]:
    texts = [chunk.content for chunk in chunks]
    embeddings = await create_embeddings(texts)

    return [
        ChunkWithEmbedding(
            chunk_index=chunk.chunk_index,
            content=chunk.content,
            embedding=embedding,
        )
        for chunk, embedding in zip(chunks, embeddings)
    ]
