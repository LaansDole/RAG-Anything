.PHONY: mock
mock:
	uv run python api/core_endpoint_test.py api/datasets/medical_symptoms_small.xlsx

.PHONY: server
server:
	@echo "Starting RAGAnything API server..."
	@echo "Server will be available at http://localhost:8000"
	@echo "Press Ctrl+C to gracefully stop the server"
	uv run uvicorn api.app:app --reload

.PHONY: dev
dev:
	@echo "Starting RAGAnything development environment..."
	@echo "1. Starting API server..."
	@uv run uvicorn api.app:app &

.PHONY: stop
stop:
	@echo "Stopping all services..."
	@pkill -f "uvicorn api.app:app" || true

.PHONY: lint
lint:
	uv run ruff check . --fix --ignore=E402

.PHONY: docker-build
docker-build:
	@docker build -t raganything .

.PHONY: docker
docker: docker-build
	@docker run -p 8000:8000 raganything
