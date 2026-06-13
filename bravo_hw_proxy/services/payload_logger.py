import json
from datetime import datetime
from typing import Any

from bravo_hw_proxy.core.config import settings
from bravo_hw_proxy.core.logging import logger

_counter = 0


def save_default_printer_payload(payload: Any, client_host: str = "unknown") -> str:
    global _counter
    _counter += 1

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    filename = settings.LOG_DIR / f"default_printer_action_{timestamp}_{_counter}.json"

    data = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "counter": _counter,
        "client_host": client_host,
        "payload": payload,
    }

    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        with open(settings.LAST_DEFAULT_PRINTER_ACTION_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logger.info("Saved default_printer_action payload to %s", filename)
        return str(filename)
    except Exception as exc:
        logger.exception("Failed to save default_printer_action payload: %s", exc)
        return ""
