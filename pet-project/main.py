import logging
from utils.timing import measure_time
from contextlib import asynccontextmanager
from core.models import db_helper
from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse
from logging_config import configure_logging
from api import router as api_router
from fastapi.middleware.cors import CORSMiddleware

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    logger.info("LOGGING CONFIGURED")
    # startup
    yield
    # shutdown
    await db_helper.dispose()


main_app = FastAPI(
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)

main_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Замените "*" на конкретные домены, если нужно
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить все методы, включая OPTIONS
    allow_headers=["*"],
)

main_app.include_router(
    api_router,
)

@main_app.middleware('http')
@measure_time
async def log_request(request: Request, call_next):
    return await call_next(request)

