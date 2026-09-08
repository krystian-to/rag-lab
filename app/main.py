from fastapi import FastAPI

from app.api.health import router as health_router
from app.config import get_settings


def create_app() -> FastAPI:
    settings = get_settings()
    application = FastAPI(
        title="PRC AI Research Assistant",
        version="0.1.0",
        debug=settings.app_env == "dev",
    )
    application.include_router(health_router)
    return application


app = create_app()

