# RAG-Anything FastAPI Service

This service exposes minimal endpoints for querying and document processing using RAG-Anything with unified LLM binding configuration.

Quick start (using uv):
- Install dev deps once (FastAPI/uvicorn):
  `uv add fastapi 'uvicorn[standard]'`
- Run the server http://127.0.0.1:8000/docs:
  `uv run uvicorn service.app:app --reload`

Environment variables `.env` (unified LLM binding approach):
- LLM_BINDING_HOST (default: http://localhost:1234/v1)
- LLM_BINDING_API_KEY (default: lm-studio)  
- LLM_MODEL (default: openai/gpt-oss-20b)
- EMBEDDING_BINDING_HOST (default: http://localhost:1234/v1)
- EMBEDDING_BINDING_API_KEY (default: lm-studio)
- EMBEDDING_MODEL (default: text-embedding-nomic-embed-text-v1.5)
- WORKING_DIR (default: ./rag_storage_service/<uuid>)

For LM Studio usage, set:
```
LLM_BINDING=lmstudio
EMBEDDING_BINDING=lmstudio
```
