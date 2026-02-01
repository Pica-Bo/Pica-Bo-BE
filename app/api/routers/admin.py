from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.util.functions.auth import internal_service_auth

router = APIRouter()
templates = Jinja2Templates(directory='templates')

@router.get('/dashboard', response_class=HTMLResponse, dependencies=[Depends(internal_service_auth)])
async def admin_dashboard(request: Request):
    context = {'request': request, 'title': 'Admin Dashboard'}
    return templates.TemplateResponse('admin/dashboard.html', context)
