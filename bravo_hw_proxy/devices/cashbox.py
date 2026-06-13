from bravo_hw_proxy.core.config import settings
from bravo_hw_proxy.core.logging import logger
from bravo_hw_proxy.devices.printer import raw_print


# Основной вариант для большинства ESC/POS-принтеров:
# ESC p m t1 t2
# m = 0 -> drawer pin 2 / kick-out connector 1
CASHBOX_PULSE = b"\x1b\x70\x00\x19\xfa"


def open_cashbox() -> bool:
    """
    Open cash drawer with one pulse only.
    """
    logger.info("Sending single cashbox pulse to printer %s", settings.PRINTER_NAME)

    return raw_print(
        settings.PRINTER_NAME,
        CASHBOX_PULSE,
        job_name="Bravo POS Cashbox Pulse",
    )