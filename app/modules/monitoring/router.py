from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from app.core.templates import templates

router = APIRouter()


@router.get("/monitor", response_class=HTMLResponse)
async def monitor_page(request: Request) -> HTMLResponse:
    items = {
        "djinni": "https://djinni.co/jobs/?search_type=basic-search&primary_keyword=Python&exp_level=no_exp&exp_level=1y&english_level=intermediate",
        "dou": "https://jobs.dou.ua/companies/precoro/vacancies/362981/?from=list_hot",
    }

    return templates.TemplateResponse(request=request, name="list.html", context={"items": items})
