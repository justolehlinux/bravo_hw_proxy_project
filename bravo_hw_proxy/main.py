import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from bravo_hw_proxy.api.routes import router
from bravo_hw_proxy.core.config import settings
from bravo_hw_proxy.core.logging import logger

app = FastAPI(title="Bravo Hardware Proxy", version="0.3.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
)

app.include_router(router)


def run() -> None:
    logger.info("Starting Bravo Hardware Proxy on http://%s:%s", settings.HOST, settings.PORT)
    logger.info("Printer: %s width=%s", settings.PRINTER_NAME, settings.PRINTER_DOTS_WIDTH)
    logger.info("Scale: %s %s 8N1 timeout=%s", settings.SCALE_PORT, settings.SCALE_BAUDRATE, settings.SCALE_TIMEOUT)
    uvicorn.run("bravo_hw_proxy.main:app", host=settings.HOST, port=settings.PORT, reload=False, log_level="info")
