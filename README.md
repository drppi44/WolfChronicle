# Hybrid RAG with FastAPI, PostgreSQL and pgvector

A Retrieval-Augmented Generation (RAG) application built from scratch using FastAPI, PostgreSQL, pgvector and OpenAI.

The project combines **semantic search** (vector embeddings) and **lexical search** (PostgreSQL Full-Text Search) using **Reciprocal Rank Fusion (RRF)** to retrieve the most relevant context before generating an answer with an LLM.

---

## Features

- Semantic search using OpenAI embeddings + pgvector
- Lexical search using PostgreSQL Full-Text Search
- Hybrid retrieval using Reciprocal Rank Fusion (RRF)
- PDF ingestion and chunking
- OpenAI-powered answer generation
- Async FastAPI application
- SQLAlchemy Async
- Alembic migrations
- Docker Compose support

---

## Tech Stack

- Python 3.12
- FastAPI
- PostgreSQL 17
- pgvector
- SQLAlchemy Async
- Alembic
- OpenAI API
- Docker
- Docker Compose

---

## Architecture

```text
                PDF
                 │
                 ▼
          Text Extraction
                 │
                 ▼
             Chunking
                 │
                 ▼
        OpenAI Embeddings
                 │
                 ▼
      PostgreSQL + pgvector
                 │
      ┌──────────┴──────────┐
      ▼                     ▼
Semantic Search      Lexical Search
 (pgvector)         (PostgreSQL FTS)
      │                     │
      └──────────┬──────────┘
                 ▼
        Reciprocal Rank Fusion
                 ▼
        Retrieved Context
                 ▼
            OpenAI GPT
                 ▼
              Answer
```

---



## Prerequisites

- Docker
- Docker Compose
- OpenAI API key

---

## Configuration

Touch a `.env` file:

```env
OPENAI_API_KEY=your_api_key_here
```

---

## Running the Project

Build containers from scratch:

```bash
docker compose build --no-cache
```

Start services:

```bash
docker compose up 
```

Run database migrations:

```bash
docker compose exec api alembic upgrade head
```

Index PDF documents:

```bash
docker compose exec api python -m app.cli ingest data/wolves.pdf
```

The API will be available at:

```
http://localhost:8000
```

Swagger UI:

```
http://localhost:8000/docs
```

---

## Example Request

Endpoint:

```
POST http://localhost:8000/ask
```

Request:

```json
{
    "question": "What do wolves eat?"
}
```

Example Response:

```json
{
    "answer": "Wolves are carnivores. They mainly hunt large hoofed mammals such as elk and deer."
}
```

---


## License

This project is licensed under the MIT License.
