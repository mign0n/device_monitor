import uvicorn

from device_monitor.config import get_settings

if __name__ == "__main__":
    app_settings = get_settings().app
    uvicorn.run(
        app="device_monitor.app:app_factory",
        host=app_settings.host,
        port=app_settings.port,
        factory=True,
        reload=app_settings.debug,
        workers=4,
    )
