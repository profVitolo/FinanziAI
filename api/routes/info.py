from fastapi import APIRouter, Request

router = APIRouter(prefix="/info", tags=["Info"])

@router.get("")
def get_info(request: Request):
    app = request.app

    return {
        "application": app.title,
        "description": app.description,
        "version": app.version
    }