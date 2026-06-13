import logging
from bravo_hw_proxy.core.config import settings

logger = logging.getLogger("bravo_hw_proxy")
logger.setLevel(logging.INFO)
logger.handlers.clear()

formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

try:
    file_handler = logging.FileHandler(settings.APP_LOG_FILE, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
except Exception as exc:
    print(f"[WARN] Could not create log file handler: {exc}")
