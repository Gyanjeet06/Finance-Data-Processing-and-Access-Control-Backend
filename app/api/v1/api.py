from fastapi import APIRouter
from app.api.v1.endpoints import auth, records, stats, users

router = APIRouter()
router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(users.router, prefix="/users", tags=["users"])
router.include_router(records.router, prefix="/records", tags=["records"])
router.include_router(stats.router, prefix="/stats", tags=["stats"])
