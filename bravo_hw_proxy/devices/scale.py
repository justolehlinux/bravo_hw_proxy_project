from bravo_hw_proxy.core.config import settings
from bravo_hw_proxy.core.logging import logger

try:
    import serial
except Exception as exc:
    serial = None
    print(f"[WARN] pyserial not available: {exc}")


def read_scale_once() -> dict:
    if serial is None:
        logger.error("pyserial is not available. Cannot read scale.")
        return {"success": False, "port": settings.SCALE_PORT, "value": None, "raw": None, "error": "pyserial not available"}

    ser = None
    try:
        ser = serial.Serial(
            port=settings.SCALE_PORT,
            baudrate=settings.SCALE_BAUDRATE,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=settings.SCALE_TIMEOUT,
        )
        raw = ser.readline()
        decoded = raw.decode("ascii", errors="replace").strip() if raw else None
        logger.info("Scale raw line: %s", decoded)
        return {"success": decoded is not None, "port": settings.SCALE_PORT, "value": decoded, "raw": decoded, "error": None if decoded else "No data from scale"}
    except Exception as exc:
        logger.exception("Scale read failed on %s: %s", settings.SCALE_PORT, exc)
        return {"success": False, "port": settings.SCALE_PORT, "value": None, "raw": None, "error": str(exc)}
    finally:
        if ser is not None:
            try:
                ser.close()
            except Exception:
                pass
