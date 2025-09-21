# RAGAnything Streamlit UI

A comprehensive web interface for the RAGAnything service providing an intuitive way to upload documents, configure processing parameters, and query your data with natural language.

## Installation

```bash
# Install UI dependencies
uv sync --extra ui

# Or install all extras including UI
uv sync --all-extras
```

## Usage

### 1. Start the RAGAnything Service
First, ensure the RAGAnything service is running:

```bash
# Using make (recommended)
make server

# Or directly with uv
uv run uvicorn api.app:app --reload

# Or with uvicorn
uvicorn api.app:app --reload
```

The service should be accessible at `http://localhost:8000`

### 2. Launch the Streamlit UI
```bash
# Using streamlit directly
streamlit run streamlit_app.py

# Or with uv
uv run streamlit run streamlit_app.py
```

The UI will be available at `http://localhost:8501`

### 3. Configure Service Connection
1. Open the Streamlit interface
2. In the sidebar, verify the "Service URL" (default: `http://localhost:8000`)
3. Click "🔗 Connect" to verify connectivity
4. Look for the "✅ Service Connected" status indicator

### 4. Upload and Process Documents
1. Navigate to the "📁 Upload" tab
2. Drag and drop files or use the file picker
3. Configure processing parameters in the sidebar (if needed)
4. Click "🚀 Process Files" to upload and process your documents

### 5. Query Your Documents
1. Go to the "🔍 Query" tab
2. Enter your question in natural language
3. Optionally add multimodal content (images, additional text)
4. Click "🚀 Ask Question" to get intelligent responses

## Configuration

### Service Settings
- **Service URL**: RAGAnything service endpoint (default: `http://localhost:8000`)
- **Query Mode**: Choose between hybrid, local, global, or naive retrieval modes

### Excel Processing Settings
- **Max Rows**: Limit number of rows processed (default: 500)
- **Convert to Text**: Convert data to natural language descriptions
- **Include Summary**: Add dataset summary to processing
- **Chunk Size**: Number of rows per processing chunk (default: 100)

### Advanced Features
- **Multimodal Queries**: Upload images and add text context for enhanced queries
- **Query History**: Review and reuse previous queries
- **Analytics**: Monitor file processing and query performance

## Supported File Formats

| Category | Extensions | Notes |
|----------|------------|-------|
| PDF | `.pdf` | Full text and multimodal extraction |
| Word Documents | `.doc`, `.docx` | Requires LibreOffice |
| PowerPoint | `.ppt`, `.pptx` | Requires LibreOffice |
| Excel | `.xls`, `.xlsx` | Specialized processing with pandas |
| Text Files | `.txt`, `.md` | Direct text processing |
| Images | `.jpg`, `.jpeg`, `.png`, `.bmp`, `.tiff`, `.tif`, `.gif`, `.webp` | Multimodal processing |

## API Endpoints Used

The Streamlit UI interacts with these RAGAnything service endpoints:

- `GET /health` - Service health check
- `POST /process-file` - General document processing
- `POST /process-excel` - Excel-specific processing
- `POST /query` - Standard text queries
- `POST /query-multimodal` - Enhanced queries with multimodal content

## License

This Streamlit interface is part of the RAGAnything project and follows the same MIT license.