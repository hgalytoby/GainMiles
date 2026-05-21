from fastapi import APIRouter

from .employee import router as employee_router
from .v1 import router as v1_router

router = APIRouter(prefix="/api")
router.include_router(v1_router)
router.include_router(employee_router)
