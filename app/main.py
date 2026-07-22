from fastapi import FastAPI

from app.db import SessionLocal
from app.rag import ask
from app.schemas import AskRequest, AskResponse


app = FastAPI()


@app.post("/ask", response_model=AskResponse)
async def ask_endpoint(request: AskRequest) -> AskResponse:
    async with SessionLocal() as session:
        answer = await ask(
            session=session,
            question=request.question,
        )

    return AskResponse(answer=answer)