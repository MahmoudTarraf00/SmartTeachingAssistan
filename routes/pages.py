from fastapi import APIRouter, Request
from fastapi.responses import FileResponse, RedirectResponse

router = APIRouter()


@router.get("/")
async def homepage(request: Request):
    if request.cookies.get("session_id"):
        return RedirectResponse(url="/page", status_code=303)
    return FileResponse("pages/Home.html")


@router.get("/login")
def login():
    return FileResponse("pages/login.html")


@router.get("/camera")
def camera_page():
    return FileResponse("pages/camera.html")


@router.get("/page")
def page():
    return FileResponse("pages/page.html")
