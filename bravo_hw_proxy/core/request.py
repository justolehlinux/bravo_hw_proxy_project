from fastapi import Request
from bravo_hw_proxy.core.logging import logger


async def get_request_payload(request: Request):
    try:
        return await request.json()
    except Exception:
        try:
            body = await request.body()
            if not body:
                return {}
            return body.decode("utf-8", errors="replace")
        except Exception as exc:
            logger.exception("Could not read request body: %s", exc)
            return {}
