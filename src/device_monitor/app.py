from fastapi import FastAPI

from device_monitor.config import get_settings
from device_monitor.routers import battery_router, device_router


def app_factory() -> FastAPI:
    """Application factory.

    Returns:
        FastAPI application instance.
    """
    app_settings = get_settings().app
    app = FastAPI(
        title=app_settings.title,
        description=app_settings.description,
        docs_url=app_settings.docs_url,
        redoc_url=app_settings.redoc_url,
        root_path=app_settings.root_path,
    )

    app.include_router(battery_router)
    app.include_router(device_router)

    return app
