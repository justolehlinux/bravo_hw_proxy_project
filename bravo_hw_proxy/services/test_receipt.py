from datetime import datetime
from bravo_hw_proxy.core.config import settings
from bravo_hw_proxy.devices.printer import raw_print


def escpos_test_receipt() -> bytes:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return b"".join([
        b"\x1b\x40",
        b"\x1b\x61\x01",
        b"\x1b\x21\x08",
        "BRAVO MARKET\n".encode("cp866", errors="replace"),
        b"\x1b\x21\x00",
        b"Hardware Proxy Test\n",
        b"\x1b\x61\x00",
        b"------------------------------\n",
        f"Time: {now}\n".encode("ascii", errors="replace"),
        f"Printer: {settings.PRINTER_NAME}\n".encode("ascii", errors="replace"),
        b"------------------------------\n",
        b"Test item              1.00\n",
        b"TOTAL                  1.00\n",
        b"------------------------------\n",
        b"\n\n\n",
        b"\x1d\x56\x42\x00",
    ])


def print_test_receipt() -> bool:
    return raw_print(settings.PRINTER_NAME, escpos_test_receipt(), job_name="Bravo POS Test Receipt")
