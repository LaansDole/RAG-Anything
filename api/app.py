import asyncio
import signal
import sys
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import router
from .core import cleanup_resources
from .utils import trigger_shutdown, cancel_all_background_tasks

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan with proper cleanup"""
    logger.info("RAG-Anything Service starting up...")

    # Set up signal handlers for graceful shutdown
    def handle_signal(signum, frame):
        logger.info(f"Received signal {signum}, initiating graceful shutdown...")
        trigger_shutdown()

        # Schedule the cleanup
        asyncio.create_task(cleanup_gracefully())

    # Register signal handlers
    if sys.platform != "win32":
        signal.signal(signal.SIGTERM, handle_signal)
        signal.signal(signal.SIGINT, handle_signal)
    else:
        # Windows signal handling
        signal.signal(signal.SIGINT, handle_signal)
        signal.signal(signal.SIGBREAK, handle_signal)

    yield

    logger.info("RAG-Anything Service shutdown complete")


async def cleanup_gracefully():
    """Cleanup resources gracefully"""
    try:
        logger.info("Cleaning up resources...")

        # Cancel all running tasks
        await cancel_all_background_tasks()

        # Cleanup core resources
        await cleanup_resources()

        logger.info("Graceful shutdown completed")

    except Exception as e:
        logger.error(f"Error during graceful shutdown: {e}")

    # Force exit if graceful shutdown takes too long
    await asyncio.sleep(1)
    sys.exit(0)


app = FastAPI(title="RAG-Anything Service", version="0.1.0", lifespan=lifespan)

# CORS for local UI dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
