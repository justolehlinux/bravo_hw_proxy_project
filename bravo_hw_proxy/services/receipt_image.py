import base64
from io import BytesIO

from PIL import Image, ImageChops, ImageOps, ImageFilter

from bravo_hw_proxy.core.config import settings
from bravo_hw_proxy.core.logging import logger
from bravo_hw_proxy.devices.printer import raw_print


def _decode_receipt_image(receipt_b64: str) -> Image.Image:
    if "," in receipt_b64 and receipt_b64.strip().startswith("data:"):
        receipt_b64 = receipt_b64.split(",", 1)[1]

    image_bytes = base64.b64decode(receipt_b64)
    image = Image.open(BytesIO(image_bytes))
    return image


def _crop_white_borders(image: Image.Image, padding: int = 2) -> Image.Image:
    """
    Агрессивная обрезка белых полей вокруг чека.
    """
    gray = image.convert("L")

    # Белый фон
    bg = Image.new("L", gray.size, 255)
    diff = ImageChops.difference(gray, bg)

    # Всё, что не почти белое - считаем содержимым
    mask = diff.point(lambda p: 255 if p > settings.RECEIPT_CONTENT_THRESHOLD else 0)

    bbox = mask.getbbox()
    if not bbox:
        return gray

    left, upper, right, lower = bbox

    left = max(0, left - padding)
    upper = max(0, upper - padding)
    right = min(gray.width, right + padding)
    lower = min(gray.height, lower + padding)

    return gray.crop((left, upper, right, lower))


def _prepare_receipt_image(image: Image.Image) -> Image.Image:
    image = image.convert("L")

    if settings.RECEIPT_ROTATE_90:
        image = image.rotate(90, expand=True)

    # Обрезаем белые поля
    image = _crop_white_borders(image, padding=settings.RECEIPT_CROP_PADDING)

    # Автоконтраст
    image = ImageOps.autocontrast(image)

    # Лёгкая резкость
    image = image.filter(ImageFilter.SHARPEN)

    target_width = settings.PRINTER_DOTS_WIDTH

    # Растягиваем на всю ширину принтера
    if image.width != target_width:
        ratio = target_width / float(image.width)
        target_height = int(image.height * ratio)
        image = image.resize((target_width, target_height), Image.Resampling.LANCZOS)

    # Ещё раз автоконтраст после resize
    image = ImageOps.autocontrast(image)

    return image


def escpos_raster_from_image(image: Image.Image) -> bytes:
    image = _prepare_receipt_image(image)

    width = image.width
    height = image.height

    bytes_per_row = (width + 7) // 8
    padded_width = bytes_per_row * 8

    if padded_width != width:
        padded = Image.new("L", (padded_width, height), 255)
        padded.paste(image, (0, 0))
        image = padded
        width = padded_width

    pixels = image.load()
    raster = bytearray()

    threshold = settings.RECEIPT_THRESHOLD

    for y in range(height):
        for x_byte in range(bytes_per_row):
            byte = 0
            for bit in range(8):
                x = x_byte * 8 + bit
                if x < width:
                    pixel = pixels[x, y]
                    if pixel < threshold:
                        byte |= 1 << (7 - bit)
            raster.append(byte)

    xL = bytes_per_row & 0xFF
    xH = (bytes_per_row >> 8) & 0xFF
    yL = height & 0xFF
    yH = (height >> 8) & 0xFF

    return b"".join([
        b"\x1b\x40",              # init
        b"\x1b\x61\x01",          # center
        b"\x1d\x76\x30\x00",      # GS v 0 raster image
        bytes([xL, xH, yL, yH]),
        bytes(raster),
        b"\x1b\x61\x00",
        b"\n\n\n",
        b"\x1d\x56\x42\x00",
    ])


def print_receipt_base64_jpeg(receipt_b64: str) -> bool:
    try:
        if not receipt_b64:
            logger.error("Empty receipt base64.")
            return False

        image = _decode_receipt_image(receipt_b64)

        logger.info(
            "Decoded receipt image: format=%s size=%sx%s mode=%s",
            image.format,
            image.width,
            image.height,
            image.mode,
        )

        escpos_data = escpos_raster_from_image(image)

        return raw_print(
            settings.PRINTER_NAME,
            escpos_data,
            job_name="Bravo POS Receipt",
        )

    except Exception as exc:
        logger.exception("Failed to print receipt image: %s", exc)
        return False