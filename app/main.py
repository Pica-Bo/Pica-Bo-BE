import os
import logging
import asyncio
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import settings
from app.api.routers import admin, auth, activity, team, team_member, user
from app.util.error_handling import DomainError

# ensure DB init runs
from app.core import db_init  # noqa: F401

load_dotenv()

app = FastAPI(title="FastAPI Beanie Jinja Starter")

logger = logging.getLogger(__name__)

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
app.include_router(user.router, prefix='/users', tags=['users'])

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

    # Check Redis connectivity via raw TCP socket
    try:
        reader, writer = await asyncio.open_connection(settings.redis_host, settings.redis_port)
        writer.close()
        await writer.wait_closed()
    except Exception as exc:  # pragma: no cover - simple health check
        logger.warning('Redis health check failed: %s', exc)
        redis_status = 'error'

    overall = 'ok' if mongo_status == 'ok' and redis_status == 'ok' else 'degraded'

    return {
        'status': overall,
        'mongo': mongo_status,
        'redis': redis_status,
    }
