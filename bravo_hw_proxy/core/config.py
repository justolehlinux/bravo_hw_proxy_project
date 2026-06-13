from pathlib import Path


class Settings:
    # =========================
    # Server
    # =========================
    HOST: str = "0.0.0.0"
    PORT: int = 9123

    # =========================
    # Odoo / IoT identity
    # =========================
    IOT_IP: str = "192.168.18.141"
    IOT_NAME: str = "Bravo Local Hardware Proxy"
    IOT_IDENTIFIER: str = "bravo-hw-proxy-windows"

    # =========================
    # Printer
    # =========================
    PRINTER_NAME: str = "POS58ENG"

    # 58mm thermal printer is usually 384 dots.
    # If receipt is too narrow/wide, tune this:
    # 384 = common 58mm
    # 576 = common 80mm
    PRINTER_DOTS_WIDTH: int = 384

    # =========================
    # Receipt image processing
    # =========================

    # Lower = less black / thinner text.
    # Higher = more black / bolder text.
    # Recommended range: 150-190
    RECEIPT_THRESHOLD: int = 165

    # Used for detecting content when cropping white borders.
    # Lower = more aggressive crop.
    # Recommended range: 8-25
    RECEIPT_CONTENT_THRESHOLD: int = 12

    # White border left around the detected receipt content.
    # Lower = bigger printed content.
    # Recommended range: 0-12
    RECEIPT_CROP_PADDING: int = 2

    # Set True only if the receipt prints sideways.
    RECEIPT_ROTATE_90: bool = False

    # =========================
    # Scale
    # =========================
    SCALE_PORT: str = "COM3"
    SCALE_BAUDRATE: int = 9600
    SCALE_TIMEOUT: int = 1

    # =========================
    # Paths
    # =========================
    BASE_DIR: Path = Path(__file__).resolve().parents[2]
    LOG_DIR: Path = BASE_DIR / "logs"

    LAST_DEFAULT_PRINTER_ACTION_FILE: Path = LOG_DIR / "last_default_printer_action.json"
    APP_LOG_FILE: Path = LOG_DIR / "bravo_hw_proxy.log"


settings = Settings()
settings.LOG_DIR.mkdir(exist_ok=True)


# ============================================================
# Backward compatibility
# Старые файлы могут импортировать переменные напрямую:
# from bravo_hw_proxy.core.config import PRINTER_NAME
#
# Новые файлы могут импортировать settings:
# from bravo_hw_proxy.core.config import settings
# ============================================================

HOST = settings.HOST
PORT = settings.PORT

IOT_IP = settings.IOT_IP
IOT_NAME = settings.IOT_NAME
IOT_IDENTIFIER = settings.IOT_IDENTIFIER

PRINTER_NAME = settings.PRINTER_NAME
PRINTER_DOTS_WIDTH = settings.PRINTER_DOTS_WIDTH

RECEIPT_THRESHOLD = settings.RECEIPT_THRESHOLD
RECEIPT_CONTENT_THRESHOLD = settings.RECEIPT_CONTENT_THRESHOLD
RECEIPT_CROP_PADDING = settings.RECEIPT_CROP_PADDING
RECEIPT_ROTATE_90 = settings.RECEIPT_ROTATE_90

SCALE_PORT = settings.SCALE_PORT
SCALE_BAUDRATE = settings.SCALE_BAUDRATE
SCALE_TIMEOUT = settings.SCALE_TIMEOUT

BASE_DIR = settings.BASE_DIR
LOG_DIR = settings.LOG_DIR
LAST_DEFAULT_PRINTER_ACTION_FILE = settings.LAST_DEFAULT_PRINTER_ACTION_FILE
APP_LOG_FILE = settings.APP_LOG_FILE