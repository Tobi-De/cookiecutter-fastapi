from fastapi import APIRouter, Request

from {{cookiecutter.project_slug}}.frontend.utils import render_html

router = APIRouter()


@router.get("/")
def index(request: Request):
    return render_html(request, "index.html")
