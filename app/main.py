import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv

from app.core.config import settings
from app.api.routers import admin, auth

# ensure DB init runs
from app.core import db_init  # noqa: F401

load_dotenv()

app = FastAPI(title="FastAPI Beanie Jinja Starter")

# Mount static and templates
app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')

# Include routers
app.include_router(admin.router, prefix='/admin', tags=['admin'])
app.include_router(auth.router, prefix='/auth', tags=['auth'])

@app.get('/health')
async def health():
    return {'status': 'ok'}
