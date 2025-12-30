from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.services.auth_service import jwt_required

router = APIRouter()
templates = Jinja2Templates(directory='templates')

@router.get('/dashboard', response_class=HTMLResponse)
async def admin_dashboard(request: Request, _=Depends(jwt_required)):
    context = {'request': request, 'title': 'Admin Dashboard'}
    return templates.TemplateResponse('admin/dashboard.html', context)
