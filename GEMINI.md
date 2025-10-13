# RAG-Anything Project Overview

This document provides a comprehensive overview of the RAG-Anything project, its structure, and how to build, run, and contribute to it.

## Project Purpose

RAG-Anything is an all-in-one multimodal Retrieval-Augmented Generation (RAG) framework built on top of LightRAG. It is designed to process a wide variety of document formats, including PDFs, Office documents, images, and text files, and to perform intelligent queries on the processed content. The framework is highly extensible, with specialized processors for different content types like images, tables, and equations.

The project consists of three main components:

1.  **`raganything` library:** The core Python library that provides the main functionality for document processing and querying.
2.  **`api`:** A FastAPI backend that exposes the functionality of the `raganything` library through a REST API.
3.  **`ui`:** A Streamlit web interface that provides a user-friendly way to interact with the RAG-Anything service.

## Building and Running

### Installation

The project uses `uv` for dependency management.

-   To install the base dependencies:
    ```bash
    uv sync
    ```
-   To install dependencies for the UI:
    ```bash
    uv sync --extra ui
    ```
-   To install all optional dependencies:
    ```bash
    uv sync --all-extras
    ```

### Running the Application

The project provides a `Makefile` with convenient commands for running the application.

-   **Run the development environment (API server and UI):**
    ```bash
    make dev
    ```
-   **Run the API server only:**
    ```bash
    make server
    ```
    The API server will be available at `http://localhost:8000`.

-   **Run the Streamlit UI only:**
    ```bash
    make ui
    ```
    The Streamlit UI will be available at `http://localhost:8501`.

-   **Stop all running services:**
    ```bash
    make stop
    ```

## Development Conventions

### Code Style and Linting

The project uses `pre-commit` with `ruff` for code formatting and linting. Before committing any changes, make sure to install the pre-commit hooks:

```bash
pre-commit install
```

The pre-commit hooks will automatically format and lint your code when you commit.

### Project Structure

-   `raganything/`: The core Python library.
    -   `raganything.py`: The main entry point for the library.
    -   `config.py`: Configuration classes.
    -   `parser.py`: Document parsing logic.
    -   `processor.py`: Content processing logic.
    -   `modalprocessors.py`: Specialized processors for multimodal content.
    -   `query.py`: Querying logic.
-   `api/`: The FastAPI application.
    -   `app.py`: The main FastAPI application.
    -   `routes.py`: API routes.
    -   `core.py`: Core API logic.
-   `ui/`: The Streamlit user interface.
    -   `streamlit_app.py`: The main Streamlit application.
-   `docs/`: Project documentation.
-   `examples/`: Example usage scripts.
-   `tests/`: (Not present, but would contain tests).

### Contribution Guidelines

When contributing to the project, please follow these guidelines:

1.  Adhere to the existing code style and conventions.
2.  Write clear and concise commit messages.
3.  Add tests for any new features or bug fixes.
4.  Update the documentation if necessary.
5.  Make sure all tests and pre-commit hooks pass before submitting a pull request.
