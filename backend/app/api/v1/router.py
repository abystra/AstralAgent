from fastapi import APIRouter

router = APIRouter(prefix="/api/v1", tags=["v1"])


@router.get("/")
async def api_root():
    """API 根路径"""
    return {"message": "API v1"}

