from fastapi import APIRouter

from src.auth.router import router as user_router

router = APIRouter()
router.include_router(router=user_router, prefix="/users")
