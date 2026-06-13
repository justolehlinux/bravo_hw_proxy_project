from typing import Any, Optional
from fastapi.responses import JSONResponse


def json_rpc_success(result: Optional[Any] = None, request_id: Any = None) -> JSONResponse:
    if result is None:
        result = {"success": True, "status": "ok"}
    return JSONResponse({"jsonrpc": "2.0", "id": request_id, "result": result})
