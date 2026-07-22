from pydantic import BaseModel


class ChunkCreate(BaseModel):
    chunk_index: int
    content: str


class ChunkWithEmbedding(ChunkCreate):
    embedding: list[float]


class AskRequest(BaseModel):
    question: str


class AskResponse(BaseModel):
    answer: str
