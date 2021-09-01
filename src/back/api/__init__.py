from fastapi import APIRouter

from .auth import router as auth_router
from .operations import router as operations_router
from .authop import router as authop_router


router = APIRouter()
router.include_router(auth_router)
router.include_router(operations_router)
router.include_router(authop_router)