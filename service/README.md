# RAG-Anything FastAPI Service

This service exposes minimal endpoints for querying and document processing using RAG-Anything with LM Studio.

Quick start (using uv):
- Install dev deps once (FastAPI/uvicorn):
  `uv add fastapi 'uvicorn[standard]'`
- Run the server http://127.0.0.1:8000/docs:
  `uv run uvicorn service.app:app --reload`

Environment variables (optional):
- LMSTUDIO_API_HOST (default: http://localhost:1234/v1)
- LMSTUDIO_API_KEY (default: lm-studio)
- MODEL_CHOICE (default: openai/gpt-oss-20b)
- EMBEDDING_MODEL_CHOICE (default: text-embedding-nomic-embed-text-v1.5)
- WORKING_DIR (default: ./rag_storage_service/<uuid>)
