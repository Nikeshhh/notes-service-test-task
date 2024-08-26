from fastapi import APIRouter

router = APIRouter(prefix="/notes")

@router.get("/")
async def root():
    return "Hello, World!"