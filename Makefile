.PHONY: server
server:
	uv run uvicorn api.app:app --reload

.PHONY: test
test:
	uv run python api/core_endpoint_test.py api/datasets/medical_symptoms_small.xlsx