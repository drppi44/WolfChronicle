from sqlalchemy.ext.asyncio import AsyncSession

from app.chunks_repository import search_hybrid
from app.embeddings import client


async def ask(
    session: AsyncSession,
    question: str,
) -> str:
    chunks = await search_hybrid(
        session=session,
        query=question,
    )
    context = "\n\n".join(
        chunk.content
        for chunk in chunks
    )

    system_prompt = """
    You are a helpful assistant.

    Answer ONLY using the provided context.

    If the answer is not in the context, say that you don't know.
    """
    user_prompt = f"""
                    Context:
                
                    {context}
                
                    Question:
                
                    {question}
    """

    response = await client.responses.create(
        model="gpt-5",
        input=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
    )
    return response.output_text