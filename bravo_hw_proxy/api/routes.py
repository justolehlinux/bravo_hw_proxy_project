import json
from fastapi import APIRouter, Request, Response

from bravo_hw_proxy.core.config import settings
from bravo_hw_proxy.core.jsonrpc import json_rpc_success
from bravo_hw_proxy.core.logging import logger
from bravo_hw_proxy.core.request import get_request_payload
from bravo_hw_proxy.devices.cashbox import open_cashbox
from bravo_hw_proxy.devices.scale import read_scale_once
from bravo_hw_proxy.services.payload_logger import save_default_printer_payload
from bravo_hw_proxy.services.receipt_image import print_receipt_base64_jpeg
from bravo_hw_proxy.services.test_receipt import print_test_receipt

router = APIRouter()


@router.options("/{full_path:path}")
async def options_all(full_path: str) -> Response:
    return Response(status_code=204)


@router.get("/")
async def root() -> dict:
    return {
        "name": "Bravo Hardware Proxy",
        "version": "0.3.0",
        "status": "ok",
        "printer": settings.PRINTER_NAME,
        "printer_dots_width": settings.PRINTER_DOTS_WIDTH,
        "scale": {"port": settings.SCALE_PORT, "baudrate": settings.SCALE_BAUDRATE, "mode": "9600 8N1"},
    }


@router.get("/hw_proxy/hello")
async def hw_proxy_hello() -> dict:
    logger.info("GET /hw_proxy/hello")
    return {
        "status": "ok",
        "message": "Bravo Hardware Proxy is alive",
        "proxy": "bravo_hw_proxy",
        "printer": settings.PRINTER_NAME,
    }


def _status_result() -> dict:
    return {
        "success": True,
        "status": "connected",
        "proxy": "bravo_hw_proxy",
        "printer": {"name": settings.PRINTER_NAME, "status": "ok"},
        "scale": {"port": settings.SCALE_PORT, "status": "configured"},
        "cashbox": {"status": "configured"},
    }


def _handshake_result() -> dict:
    return {
        "success": True,
        "status": "connected",
        "proxy": "bravo_hw_proxy",
        "iot_box": {
            "name": settings.IOT_NAME,
            "identifier": settings.IOT_IDENTIFIER,
            "ip": settings.IOT_IP,
            "port": settings.PORT,
        },
        "drivers": {"printer": True, "cashbox": True, "scale": True},
    }


@router.get("/hw_proxy/status_json")
async def status_json_get():
    return json_rpc_success(_status_result())


@router.post("/hw_proxy/status_json")
async def status_json_post(request: Request):
    payload = await get_request_payload(request)
    request_id = payload.get("id") if isinstance(payload, dict) else None
    logger.info("status_json payload: %s", payload)
    return json_rpc_success(_status_result(), request_id=request_id)


@router.get("/hw_proxy/handshake")
async def handshake_get():
    return json_rpc_success(_handshake_result())


@router.post("/hw_proxy/handshake")
async def handshake_post(request: Request):
    payload = await get_request_payload(request)
    request_id = payload.get("id") if isinstance(payload, dict) else None
    logger.info("handshake payload: %s", payload)
    return json_rpc_success(_handshake_result(), request_id=request_id)


@router.post("/hw_proxy/default_printer_action")
async def default_printer_action(request: Request):
    payload = await get_request_payload(request)
    request_id = payload.get("id") if isinstance(payload, dict) else None
    client_host = request.client.host if request.client else "unknown"

    logger.info("default_printer_action received from client=%s", client_host)
    try:
        logger.info(json.dumps(payload, ensure_ascii=False, indent=2)[:5000])
    except Exception:
        logger.info("%s", payload)

    saved_file = save_default_printer_payload(payload, client_host)

    data = payload.get("params", {}).get("data", {}) if isinstance(payload, dict) else {}
    action = data.get("action")
    logger.info("default_printer_action action=%s", action)

    result = {
        "success": True,
        "action": action,
        "payload_saved_to": saved_file,
        "cashbox_opened": False,
        "receipt_printed": False,
    }

    try:
        if action == "cashbox":
            result["cashbox_opened"] = open_cashbox()
        elif action == "print_receipt":
            result["receipt_printed"] = print_receipt_base64_jpeg(data.get("receipt"))
        else:
            logger.warning("Unknown default_printer_action action: %s", action)
    except Exception as exc:
        logger.exception("default_printer_action failed internally: %s", exc)

    return json_rpc_success(result, request_id=request_id)


@router.post("/test/print")
async def test_print():
    printed = print_test_receipt()
    return json_rpc_success({"success": True, "printed": printed, "printer": settings.PRINTER_NAME})


@router.post("/test/cashbox")
async def test_cashbox():
    opened = open_cashbox()
    return json_rpc_success({"success": True, "cashbox_pulse_sent": opened, "printer": settings.PRINTER_NAME})


@router.get("/test/scale")
async def test_scale():
    return json_rpc_success({"success": True, "scale": read_scale_once()})
