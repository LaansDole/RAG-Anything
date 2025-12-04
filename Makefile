.PHONY: mock
mock:
	uv run python api/core_endpoint_test.py api/datasets/medical_symptoms_small.xlsx

.PHONY: ui
ui:
	uv run streamlit run ui/streamlit_app.py

.PHONY: install-ui
install-ui:
	uv sync --extra ui

.PHONY: dev
dev:
	@echo "Starting RAGAnything development environment..."
	@echo "1. Starting API server..."
	@uv run uvicorn api.app:app &
	@sleep 3
	@echo "2. Starting Streamlit UI..."
	@uv run streamlit run ui/streamlit_app.py

.PHONY: stop
stop:
	@echo "Stopping all services..."
	@pkill -f "uvicorn api.app:app" || true
	@pkill -f "streamlit run ui/streamlit_app.py" || true

.PHONY: lint
lint:
	uv run ruff check . --fix --ignore=E402

.PHONY: docker-build
docker-build:
	@docker build -t raganything .

.PHONY: docker
docker: docker-build
	@docker run -p 8000:8000 raganything
