import asyncio
import sys
from pathlib import Path

from app.db import SessionLocal
from app.ingest import ingest
from app.chunks_repository import search_semantic
from app.rag import ask


async def main():
    command = sys.argv[1]

    if command == "ingest":
        await ingest(Path(sys.argv[2]))

    elif command == "search":
        query = " ".join(sys.argv[2:])

        async with SessionLocal() as session:
            chunks = await search_semantic(
                session=session,
                query=query,
                limit=10,
            )

            for chunk in chunks:
                print("=" * 80)
                print(f"Chunk #{chunk.chunk_index}")
                print(chunk.content)

    elif command == "ask":
        if len(sys.argv) < 3:
            raise SystemExit("Usage: python -m app.cli ask <question>")

        question = " ".join(sys.argv[2:])

        async with SessionLocal() as session:
            answer = await ask(
                session=session,
                question=question,
            )

        print(answer)
    else:
        raise ValueError(f"Unknown command: {command}")


if __name__ == "__main__":
    asyncio.run(main())
