from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from app.core.templates import templates

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def dashboard_page(request: Request) -> HTMLResponse:
    stats = {"active_monitors": 12, "changes_today": 3, "failed_checks": 1, "checks_today": 42}

    return templates.TemplateResponse(
        request=request, name="dashboard.html", context={"stats": stats}
    )
