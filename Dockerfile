# Multi-stage build for RAG-Anything
FROM python:3.10-slim AS builder

# Set environment variables for non-interactive installation
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV UV_CACHE_DIR=/tmp/uv-cache

# Install minimal system dependencies
# Only curl is needed for health checks and basic operations
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv for faster package management
RUN pip install uv

# Set working directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Copy source code for version discovery
COPY raganything/ ./raganything/

# Install Python dependencies using uv
RUN uv sync --frozen --extra ui --no-dev

# Production stage
FROM python:3.10-slim AS production

# Install runtime system dependencies
# Only curl is needed for health checks; LibreOffice is external dependency
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash raguser

# Install uv in production stage
RUN pip install uv

# Set working directory
WORKDIR /app

# Copy dependency files and source code
COPY pyproject.toml uv.lock ./
COPY raganything/ ./raganything/

# Install Python dependencies using uv
RUN uv sync --frozen --extra ui --no-dev

# Copy application code
COPY --chown=raguser:raguser . .

# Set ownership of app directory
RUN chown -R raguser:raguser /app

# Switch to non-root user
USER raguser

# Set environment variables for production
ENV PATH=/app/.venv/bin:$PATH
ENV UV_CACHE_DIR=/tmp/uv-cache
ENV PYTHONPATH=/app

# Expose port for API service
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Default command
CMD ["uv", "run", "uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "8000"]
