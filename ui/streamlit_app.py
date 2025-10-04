#!/usr/bin/env python
"""
RAGAnything Streamlit Application

A comprehensive web interface for the RAGAnything service providing:
- Document upload and processing
- Query interface with multimodal support
- Parameter configuration
- Response visualization
- Session state management
"""

import streamlit as st
import requests
import time
import pandas as pd
from pathlib import Path
from typing import Dict, List, Any

# Configuration
DEFAULT_SERVICE_URL = "http://localhost:8000"
MAX_FILE_SIZE_MB = 100  # Maximum file size in MB
ENABLE_EXCEL_PROCESSING = False  # Enable Excel-specific processing options

# API-compatible file types (removed images as API has enable_image_processing=False)
SUPPORTED_FILE_TYPES = {
    "PDF": [".pdf"],
    "Word Documents": [".doc", ".docx"],
    "PowerPoint": [".ppt", ".pptx"],
    "Excel": [".xls", ".xlsx"],
    "Text Files": [".txt", ".md"],
}

# Note: Image processing is disabled in the API (enable_image_processing=False)
# Uncomment below if image processing gets enabled in the API
# "Images": [".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".tif", ".gif", ".webp"]

# Page configuration
st.set_page_config(
    page_title="RAGAnything Service UI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown(
    """
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .upload-box {
        border: 2px dashed #cccccc;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #667eea;
    }
    .chat-container {
        max-height: 400px;
        overflow-y: auto;
        padding: 1rem;
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        background-color: #fafafa;
        margin-bottom: 1rem;
    }
    .chat-welcome {
        text-align: center;
        padding: 2rem;
        color: #666;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 15px;
        margin: 1rem 0;
    }
    .quick-action-btn {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        margin: 0.25rem;
        border: none;
        cursor: pointer;
        transition: transform 0.2s;
    }
    .quick-action-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .chat-input {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        padding: 0.75rem;
        font-size: 1rem;
    }
    .chat-input:focus {
        border-color: #667eea;
        outline: none;
        box-shadow: 0 0 10px rgba(102, 126, 234, 0.3);
    }
</style>
""",
    unsafe_allow_html=True,
)


# Initialize session state
def initialize_session_state():
    """Initialize session state variables"""
    default_state = {
        "service_url": DEFAULT_SERVICE_URL,
        "uploaded_files": [],
        "processing_status": {},
        "query_history": [],
        "current_tab": "upload",
        "advanced_settings": False,
        "last_query_result": None,
        "multimodal_content": [],
        "service_connected": False,
        "file_processing_complete": False,
        # Chatbot-specific state
        "chat_history": [],
        "current_message": "",
        "conversation_id": str(time.time()),
        "auto_scroll": True,
    }

    for key, value in default_state.items():
        if key not in st.session_state:
            st.session_state[key] = value


# Service connection functions
def check_service_health(service_url: str) -> Dict[str, Any]:
    """Check if the RAGAnything service is running"""
    try:
        response = requests.get(f"{service_url}/health", timeout=5)
        if response.status_code == 200:
            return {"status": "connected", "message": "Service is running"}
        else:
            return {
                "status": "error",
                "message": f"Service returned status {response.status_code}",
            }
    except requests.exceptions.RequestException as e:
        return {"status": "error", "message": f"Cannot connect to service: {str(e)}"}


def upload_and_process_file(file, service_url: str, file_type: str) -> Dict[str, Any]:
    """Upload and process a file through the service with enhanced error handling"""
    try:
        # Validate file size (convert bytes to MB)
        file_size_mb = file.size / (1024 * 1024)
        if file_size_mb > MAX_FILE_SIZE_MB:
            return {
                "status": "error",
                "message": f"File too large ({file_size_mb:.1f}MB). Maximum size is {MAX_FILE_SIZE_MB}MB.",
            }

        # Determine endpoint based on file type
        # This endpoint will require more power for Excel processing and may take longer
        if file_type in [".xlsx", ".xls", ".csv"] and ENABLE_EXCEL_PROCESSING:
            endpoint = f"{service_url}/process-excel"
            files = {
                "file": (
                    file.name,
                    file.getvalue(),
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )
            }
            data = {
                "max_rows": st.session_state.get("excel_max_rows", 500),
                "convert_to_text": str(
                    st.session_state.get("excel_convert_to_text", True)
                ).lower(),
                "include_summary": str(
                    st.session_state.get("excel_include_summary", True)
                ).lower(),
                "chunk_size": st.session_state.get("excel_chunk_size", 100),
            }
            # Add missing parameters if available
            if st.session_state.get("excel_sheet_name"):
                data["sheet_name"] = st.session_state.get("excel_sheet_name")
            if st.session_state.get("excel_doc_id"):
                data["doc_id"] = st.session_state.get("excel_doc_id")
        else:
            endpoint = f"{service_url}/process-file"
            files = {"file": (file.name, file.getvalue(), "application/octet-stream")}
            data = {}

        response = requests.post(endpoint, files=files, data=data, timeout=600)

        # Handle specific HTTP status codes
        if response.status_code == 200:
            # Validate JSON response
            try:
                if response.headers.get("content-type", "").startswith(
                    "application/json"
                ):
                    result = response.json()
                    result["status"] = "success"
                    return result
                else:
                    return {
                        "status": "error",
                        "message": "Invalid response format from server",
                    }
            except ValueError as e:
                return {
                    "status": "error",
                    "message": f"Invalid JSON response from server: {str(e)}",
                }
        elif response.status_code == 413:
            return {
                "status": "error",
                "message": "File too large for server. Try reducing file size or splitting into smaller files.",
            }
        elif response.status_code == 429:
            return {
                "status": "error",
                "message": "Server is overloaded. Please wait a moment and try again.",
            }
        elif response.status_code == 503:
            return {
                "status": "error",
                "message": "Service temporarily unavailable. Please try again later.",
            }
        else:
            return {
                "status": "error",
                "message": f"Upload failed: HTTP {response.status_code} - {response.text[:200]}",
            }

    except requests.exceptions.Timeout:
        return {
            "status": "error",
            "message": "Upload timeout. File may be too large or server is busy. Please try again.",
        }
    except requests.exceptions.ConnectionError:
        return {
            "status": "error",
            "message": "Cannot connect to service. Please check if the server is running and the URL is correct.",
        }
    except Exception as e:
        return {"status": "error", "message": f"Unexpected error: {str(e)}"}


def _try_multimodal_query(
    query: str, service_url: str, mode: str, multimodal_content: List[Dict]
) -> Dict[str, Any]:
    """Attempt multimodal query with proper error handling"""
    try:
        # Filter out image content since API has enable_image_processing=False
        filtered_content = []
        for content in multimodal_content:
            if content.get("type") == "text":
                filtered_content.append(content)
            elif content.get("type") == "image":
                # Skip images but log for user feedback
                continue

        if not filtered_content:
            # No valid multimodal content, fall back to standard query
            return None

        payload = {"query": query, "mode": mode, "multimodal_content": filtered_content}

        response = requests.post(
            f"{service_url}/query-multimodal", json=payload, timeout=600
        )

        if response.status_code == 200:
            result = response.json()
            result["status"] = "success"
            return result
        elif response.status_code == 501:
            # Method not implemented, fall back to standard query
            return None
        else:
            # Other errors, fall back but log the attempt
            return None

    except Exception:
        # Any exception, fall back to standard query
        return None


def _try_standard_query(query: str, service_url: str, mode: str) -> Dict[str, Any]:
    """Attempt standard query with comprehensive error handling"""
    try:
        payload = {"query": query, "mode": mode}

        response = requests.post(f"{service_url}/query", json=payload, timeout=600)

        if response.status_code == 200:
            # Validate JSON response
            try:
                if response.headers.get("content-type", "").startswith(
                    "application/json"
                ):
                    result = response.json()
                    result["status"] = "success"
                    return result
                else:
                    return {
                        "status": "error",
                        "message": "Invalid response format from server",
                    }
            except ValueError as e:
                return {
                    "status": "error",
                    "message": f"Invalid JSON response from server: {str(e)}",
                }
        elif response.status_code == 413:
            return {
                "status": "error",
                "message": "Query too large for server. Try shortening your question.",
            }
        elif response.status_code == 429:
            return {
                "status": "error",
                "message": "Server is overloaded. Please wait a moment and try again.",
            }
        elif response.status_code == 503:
            return {
                "status": "error",
                "message": "Service temporarily unavailable. Please try again later.",
            }
        else:
            return {
                "status": "error",
                "message": f"Query failed: HTTP {response.status_code} - {response.text[:200]}",
            }

    except requests.exceptions.Timeout:
        return {
            "status": "error",
            "message": "Query timeout. Please try again with a simpler question.",
        }
    except requests.exceptions.ConnectionError:
        return {
            "status": "error",
            "message": "Cannot connect to service. Please check if the server is running and the URL is correct.",
        }
    except Exception as e:
        return {"status": "error", "message": f"Unexpected error: {str(e)}"}


def query_service(
    query: str,
    service_url: str,
    mode: str = "hybrid",
    multimodal_content: List[Dict] = None,
) -> Dict[str, Any]:
    """Query the RAGAnything service with multimodal fallback support"""

    # First, try multimodal query if content is provided
    if multimodal_content and len(multimodal_content) > 0:
        multimodal_result = _try_multimodal_query(
            query, service_url, mode, multimodal_content
        )
        if multimodal_result is not None:
            return multimodal_result
        # If multimodal failed, fall back to standard query

    # Standard query (either as fallback or primary)
    return _try_standard_query(query, service_url, mode)


# UI Components
def render_sidebar():
    """Render the sidebar with configuration options"""
    st.sidebar.markdown("## ⚙️ Configuration")

    # Service URL configuration
    st.session_state.service_url = st.sidebar.text_input(
        "Service URL",
        value=st.session_state.service_url,
        help="URL of the RAGAnything service",
    )

    # Check service connection
    if st.sidebar.button("🔗 Connect"):
        with st.sidebar:
            with st.spinner("Testing connection..."):
                health = check_service_health(st.session_state.service_url)
                if health["status"] == "connected":
                    st.success(health["message"])
                    st.session_state.service_connected = True
                else:
                    st.error(health["message"])
                    st.session_state.service_connected = False

    # Connection status indicator
    if st.session_state.service_connected:
        st.sidebar.success("✅ Service Connected")
    else:
        st.sidebar.error("❌ Service Disconnected")

    st.sidebar.markdown("---")

    # Advanced settings toggle
    st.session_state.advanced_settings = st.sidebar.checkbox(
        "🔧 Advanced Settings", value=st.session_state.advanced_settings
    )

    if st.session_state.advanced_settings:
        st.sidebar.markdown("### Query Settings")

        # Query mode selection
        st.session_state.query_mode = st.sidebar.selectbox(
            "Query Mode",
            options=["hybrid", "local", "global", "naive"],
            index=0,
            help="Query mode for RAG retrieval",
        )

        st.sidebar.markdown("### Excel Processing Settings")

        # Excel-specific settings
        st.session_state.excel_max_rows = st.sidebar.number_input(
            "Max Rows",
            min_value=1,
            max_value=10000,
            value=500,
            help="Maximum number of rows to process from Excel files",
        )

        st.session_state.excel_convert_to_text = st.sidebar.checkbox(
            "Convert to Text", value=True, help="Convert Excel data to natural language"
        )

        st.session_state.excel_include_summary = st.sidebar.checkbox(
            "Include Summary", value=True, help="Include dataset summary in processing"
        )

        st.session_state.excel_chunk_size = st.sidebar.number_input(
            "Chunk Size",
            min_value=10,
            max_value=1000,
            value=100,
            help="Number of rows per chunk",
        )

    st.sidebar.markdown("---")

    # File processing status
    if st.session_state.uploaded_files:
        st.sidebar.markdown("### 📁 Processed Files")
        for file_info in st.session_state.uploaded_files:
            status_icon = "✅" if file_info.get("processed", False) else "⏳"
            st.sidebar.write(f"{status_icon} {file_info['name']}")


def render_file_upload():
    """Render the file upload interface"""
    st.markdown(
        '<h2 class="main-header">📁 Document Upload & Processing</h2>',
        unsafe_allow_html=True,
    )

    # File upload section
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("### Upload Documents")

        # Get all supported extensions
        all_extensions = []
        for extensions in SUPPORTED_FILE_TYPES.values():
            all_extensions.extend(extensions)

        uploaded_files = st.file_uploader(
            "Choose files to upload",
            type=[ext.lstrip(".") for ext in all_extensions],
            accept_multiple_files=True,
            help="Supported formats: PDF, Word, PowerPoint, Excel, Text files, and Images",
        )

        if uploaded_files:
            st.markdown("### 📋 Selected Files")
            for file in uploaded_files:
                file_ext = Path(file.name).suffix.lower()
                file_type = next(
                    (k for k, v in SUPPORTED_FILE_TYPES.items() if file_ext in v),
                    "Other",
                )

                col_file, col_size, col_type = st.columns([3, 1, 1])
                with col_file:
                    st.write(f"📄 {file.name}")
                with col_size:
                    st.write(f"{file.size / 1024:.1f} KB")
                with col_type:
                    st.write(file_type)

    with col2:
        st.markdown("### 📊 Supported Formats")
        for file_type, extensions in SUPPORTED_FILE_TYPES.items():
            st.write(f"**{file_type}**")
            st.write(", ".join(extensions))
            st.write("")

    # Process files button
    if uploaded_files and st.button("🚀 Process Files", type="primary"):
        if not st.session_state.service_connected:
            st.error("Please connect to the service first!")
            return

        progress_bar = st.progress(0)
        status_container = st.container()

        processed_files = []
        total_files = len(uploaded_files)

        for i, file in enumerate(uploaded_files):
            file_ext = Path(file.name).suffix.lower()

            with status_container:
                st.info(f"Processing {file.name}...")

            result = upload_and_process_file(
                file, st.session_state.service_url, file_ext
            )

            file_info = {
                "name": file.name,
                "size": file.size,
                "type": file_ext,
                "processed": result["status"] == "success",
                "result": result,
            }

            processed_files.append(file_info)
            progress_bar.progress((i + 1) / total_files)

            with status_container:
                if result["status"] == "success":
                    st.success(f"✅ {file.name} processed successfully!")
                    if file_ext in [".xlsx", ".xls"] and "total_rows" in result:
                        st.write(
                            f"   📊 Rows: {result['total_rows']}, Chunks: {result.get('chunks_created', 'N/A')}"
                        )
                else:
                    st.error(f"❌ Error processing {file.name}: {result['message']}")

        # Update session state
        st.session_state.uploaded_files = processed_files
        st.session_state.file_processing_complete = any(
            f["processed"] for f in processed_files
        )

        if st.session_state.file_processing_complete:
            st.balloons()
            st.success("🎉 File processing complete! You can now query your documents.")


def render_chat_message(message: Dict[str, Any], is_user: bool = True):
    """Render a chat message with appropriate styling"""
    if is_user:
        # User message (right-aligned, blue)
        st.markdown(
            f"""
        <div style="display: flex; justify-content: flex-end; margin-bottom: 1rem;">
            <div style="background-color: #007bff; color: white; padding: 0.75rem 1rem;
                        border-radius: 15px 15px 5px 15px; max-width: 70%;
                        word-wrap: break-word;">
                <strong>You:</strong><br>{message['content']}
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )
    else:
        # Assistant message (left-aligned, gray)
        timestamp = time.strftime(
            "%H:%M", time.localtime(message.get("timestamp", time.time()))
        )
        status = message.get("status", "success")

        if status == "success":
            color = "#f8f9fa"
            border_color = "#28a745"
            content = message["content"]
        else:
            color = "#f8d7da"
            border_color = "#dc3545"
            content = f"❌ Error: {message['content']}"

        st.markdown(
            f"""
        <div style="display: flex; justify-content: flex-start; margin-bottom: 1rem;">
            <div style="background-color: {color}; color: #333; padding: 0.75rem 1rem;
                        border-radius: 15px 15px 15px 5px; max-width: 80%;
                        border-left: 4px solid {border_color}; word-wrap: break-word;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                    <strong>Assistant:</strong>
                    <small style="color: #666;">{timestamp}</small>
                </div>
                {content}
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )


def render_query_interface():
    """Render the chatbot Q&A interface"""
    st.markdown(
        '<h2 class="main-header">💬 RAG Assistant Chatbot</h2>', unsafe_allow_html=True
    )

    if not st.session_state.file_processing_complete:
        st.warning(
            "⚠️ Please upload and process files first before starting a conversation."
        )
        return

    # Chat controls
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

    with col1:
        if st.button("🗑️ Clear Chat", help="Clear conversation history"):
            st.session_state.chat_history = []
            st.session_state.conversation_id = str(time.time())
            st.rerun()

    with col2:
        if st.button("📥 Export Chat", help="Export conversation to text"):
            if st.session_state.chat_history:
                export_text = generate_chat_export()
                st.download_button(
                    label="💾 Download",
                    data=export_text,
                    file_name=f"rag_chat_{st.session_state.conversation_id}.txt",
                    mime="text/plain",
                )

    chat_container = st.container()
    with chat_container:
        if st.session_state.chat_history:
            for message in st.session_state.chat_history:
                if message["role"] == "user":
                    render_chat_message({"content": message["content"]}, is_user=True)
                else:
                    render_chat_message(message, is_user=False)

    # Additional context section (collapsed by default)
    # with st.expander("📝 Add Additional Context (Optional)"):
    #     additional_context = st.text_area(
    #         "Additional Context",
    #         height=80,
    #         help="Add extra context or specific instructions to enhance your query",
    #         placeholder="E.g., 'Focus on financial data' or 'Consider only data from 2023'"
    #     )
    #     if additional_context:
    #         st.session_state.multimodal_content = [{"type": "text", "text": additional_context}]
    #     else:
    #         st.session_state.multimodal_content = []

    # Use current_message if set by quick actions
    default_message = st.session_state.get("current_message", "")
    if default_message:
        st.session_state.current_message = ""  # Clear after use

    user_input = st.text_area(
        "Type your question:",
        height=100,
        placeholder="Ask me anything about your documents...",
        value=default_message,
        help="Ask questions about content, request summaries, or seek insights from your documents",
    )

    # Send button
    send_col1, send_col2 = st.columns([3, 1])

    with send_col2:
        send_button = st.button("📤 Send", type="primary", use_container_width=True)

    # Process message
    if send_button and user_input.strip():
        if not st.session_state.service_connected:
            st.error("❌ Please connect to the service first!")
            return

        # Add user message to chat
        user_message = {
            "role": "user",
            "content": user_input.strip(),
            "timestamp": time.time(),
        }
        st.session_state.chat_history.append(user_message)

        # Show processing indicator
        with st.spinner("Thinking..."):
            mode = st.session_state.get("query_mode", "hybrid")
            multimodal = st.session_state.get("multimodal_content", [])

            result = query_service(
                user_input.strip(), st.session_state.service_url, mode, multimodal
            )

            # Add assistant response to chat
            if result["status"] == "success":
                assistant_message = {
                    "role": "assistant",
                    "content": result.get(
                        "result",
                        "I received your question but couldn't generate a response.",
                    ),
                    "timestamp": time.time(),
                    "status": "success",
                    "mode": mode,
                    "has_multimodal": len(multimodal) > 0,
                }
            else:
                assistant_message = {
                    "role": "assistant",
                    "content": result.get("message", "An unknown error occurred."),
                    "timestamp": time.time(),
                    "status": "error",
                    "mode": mode,
                    "has_multimodal": len(multimodal) > 0,
                }

            st.session_state.chat_history.append(assistant_message)

            # Add to legacy query history for compatibility
            st.session_state.query_history.append(
                {
                    "query": user_input.strip(),
                    "result": result,
                    "timestamp": time.time(),
                    "mode": mode,
                    "has_multimodal": len(multimodal) > 0,
                }
            )

        # Auto-scroll and refresh
        if st.session_state.auto_scroll:
            st.rerun()


def generate_chat_export() -> str:
    """Generate exportable text format of the chat conversation"""
    export_lines = [
        "RAG Assistant Conversation Export",
        f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}",
        f"Conversation ID: {st.session_state.conversation_id}",
        "=" * 50,
        "",
    ]

    for message in st.session_state.chat_history:
        timestamp = time.strftime("%H:%M:%S", time.localtime(message["timestamp"]))
        if message["role"] == "user":
            export_lines.extend([f"[{timestamp}] USER:", message["content"], ""])
        else:
            status_indicator = "✓" if message.get("status") == "success" else "✗"
            mode_info = (
                f" (Mode: {message.get('mode', 'unknown')})"
                if message.get("mode")
                else ""
            )
            export_lines.extend(
                [
                    f"[{timestamp}] ASSISTANT {status_indicator}{mode_info}:",
                    message["content"],
                    "",
                ]
            )

    return "\n".join(export_lines)


def render_query_results(query_result: Dict[str, Any]):
    """Render query results with proper formatting"""
    st.markdown("---")
    st.markdown("### 💬 Query Results")

    # Query info
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.write(f"**Query:** {query_result['query']}")
    with col2:
        st.write(f"**Mode:** {query_result['mode']}")
    with col3:
        multimodal_indicator = "🖼️ Yes" if query_result["has_multimodal"] else "📝 No"
        st.write(f"**Multimodal:** {multimodal_indicator}")

    # Results
    result = query_result["result"]
    if result["status"] == "success":
        st.markdown('<div class="success-box">', unsafe_allow_html=True)
        st.markdown("**Answer:**")
        st.markdown(result.get("result", "No answer provided"))
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown('<div class="error-box">', unsafe_allow_html=True)
        st.error(f"Error: {result['message']}")
        st.markdown("</div>", unsafe_allow_html=True)


def render_query_history():
    """Render query history"""
    st.markdown('<h2 class="main-header">Query History</h2>', unsafe_allow_html=True)

    if not st.session_state.query_history:
        st.info(
            "No queries executed yet. Go to the Query tab to start asking questions!"
        )
        return

    # Clear history button
    if st.button("🗑️ Clear History"):
        st.session_state.query_history = []
        st.rerun()

    # Display history in reverse order (newest first)
    for i, query_result in enumerate(reversed(st.session_state.query_history)):
        timestamp = time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime(query_result["timestamp"])
        )

        with st.expander(
            f"Query {len(st.session_state.query_history) - i}: {query_result['query'][:50]}... ({timestamp})"
        ):
            render_query_results(query_result)


def render_analytics():
    """Render analytics and statistics"""
    st.markdown('<h2 class="main-header">Analytics</h2>', unsafe_allow_html=True)

    # File processing statistics
    if st.session_state.uploaded_files:
        st.markdown("### 📁 File Processing Statistics")

        processed_count = sum(
            1 for f in st.session_state.uploaded_files if f["processed"]
        )
        total_count = len(st.session_state.uploaded_files)
        total_size = sum(f["size"] for f in st.session_state.uploaded_files)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Total Files", total_count)
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Processed", processed_count)
            st.markdown("</div>", unsafe_allow_html=True)

        with col3:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Success Rate", f"{(processed_count/total_count*100):.1f}%")
            st.markdown("</div>", unsafe_allow_html=True)

        with col4:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Total Size", f"{total_size/1024:.1f} KB")
            st.markdown("</div>", unsafe_allow_html=True)

        # File details table
        st.markdown("### 📋 File Details")
        file_data = []
        for file_info in st.session_state.uploaded_files:
            file_data.append(
                {
                    "File Name": file_info["name"],
                    "Type": file_info["type"],
                    "Size (KB)": f"{file_info['size']/1024:.1f}",
                    "Status": "✅ Processed" if file_info["processed"] else "❌ Failed",
                    "Details": file_info["result"].get("message", "")
                    if not file_info["processed"]
                    else "Success",
                }
            )

        if file_data:
            df = pd.DataFrame(file_data)
            st.dataframe(df, width="stretch")

    # Query statistics
    if st.session_state.query_history:
        st.markdown("### 🔍 Query Statistics")

        total_queries = len(st.session_state.query_history)
        successful_queries = sum(
            1
            for q in st.session_state.query_history
            if q["result"]["status"] == "success"
        )
        multimodal_queries = sum(
            1 for q in st.session_state.query_history if q["has_multimodal"]
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Total Queries", total_queries)
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Success Rate", f"{(successful_queries/total_queries*100):.1f}%")
            st.markdown("</div>", unsafe_allow_html=True)

        with col3:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Multimodal Queries", multimodal_queries)
            st.markdown("</div>", unsafe_allow_html=True)

        # Query modes distribution
        mode_counts = {}
        for query in st.session_state.query_history:
            mode = query["mode"]
            mode_counts[mode] = mode_counts.get(mode, 0) + 1

        if mode_counts:
            st.markdown("### 📊 Query Mode Distribution")
            mode_df = pd.DataFrame(list(mode_counts.items()), columns=["Mode", "Count"])
            st.bar_chart(mode_df.set_index("Mode"))


def main():
    """Main application function"""
    # Initialize session state
    initialize_session_state()

    # Render sidebar
    render_sidebar()

    # Main content area
    st.title("RAGAnything Service Interface")
    st.markdown(
        "A comprehensive interface for document processing and intelligent querying"
    )

    # Tab navigation
    tab1, tab2, tab3, tab4 = st.tabs(
        ["📁 Upload", "🔍 Query", "📚 History", "📈 Analytics"]
    )

    with tab1:
        render_file_upload()

    with tab2:
        render_query_interface()

    with tab3:
        render_query_history()

    with tab4:
        render_analytics()


if __name__ == "__main__":
    main()
