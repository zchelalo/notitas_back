from fastapi import APIRouter

from routes.v1.index import router as v1Router

router = APIRouter()

router.include_router(v1Router, prefix="/v1")