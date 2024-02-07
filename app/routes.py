from app import config
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory=config.Settings().TEMPLATE_DIR)
router = APIRouter()


@router.get("/")
def index(request: Request):
    return templates.TemplateResponse('main.html', {'request': request})