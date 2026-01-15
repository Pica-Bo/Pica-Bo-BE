import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
import redis.asyncio as redis

from app.core.config import settings
from app.api.routers import admin, auth, activity, team, team_member, operator, lookups
from app.util.error_handling import DomainError

# ensure DB init runs
from app.core import db_init  # noqa: F401

load_dotenv()

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage app lifespan: setup Redis connection pool on startup, close on shutdown."""
    # Startup: Create Redis connection pool
    app.state.redis = redis.from_url(settings.redis_url, decode_responses=True)
    logger.info(f"Redis client connected to {settings.redis_url}")
    yield
    # Shutdown: Close connections
    await app.state.redis.close()
    logger.info("Redis client closed")


app = FastAPI(title="PicaBo Backend", lifespan=lifespan)

# Mount static and templates
app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')

@app.exception_handler(DomainError)
async def domain_error_handler(request: Request, exc: DomainError):
    payload = {"code": exc.code, "message": exc.message}
    if exc.details:
        payload["details"] = exc.details
    logger.warning("Domain error (%s): %s", exc.code, payload)
    return JSONResponse(status_code=exc.status_code, content=payload)


# Include routers
app.include_router(admin.router, prefix='/admin', tags=['admin'])
app.include_router(auth.router, prefix='/auth', tags=['auth'])
app.include_router(activity.router, prefix='/activities', tags=['activities'])
app.include_router(team.router, prefix='/teams', tags=['teams'])
app.include_router(team_member.router, prefix='/team-members', tags=['team_members'])
app.include_router(operator.router, prefix='/operators', tags=['operators'])
app.include_router(lookups.router, prefix='/lookups', tags=['lookups'])

@app.get('/health')
async def health():
    mongo_status = 'ok'
    redis_status = 'ok'

    # Check MongoDB connectivity
    try:
        client = AsyncIOMotorClient(settings.mongo_uri)
        await client.admin.command('ping')
    except Exception as exc:  # pragma: no cover - simple health check
        logger.warning('MongoDB health check failed: %s', exc)
        mongo_status = 'error'

    # Check Redis connectivity using actual Redis client
    try:
        await app.state.redis.ping()
    except Exception as exc:  # pragma: no cover - simple health check
        logger.warning('Redis health check failed: %s', exc)
        redis_status = 'error'

    overall = 'ok' if mongo_status == 'ok' and redis_status == 'ok' else 'degraded'

    return {
        'status': overall,
        'mongo': mongo_status,
        'redis': redis_status,
    }
