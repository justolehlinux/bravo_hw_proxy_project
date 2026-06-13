from bravo_hw_proxy.core.logging import logger

try:
    import win32print
except Exception as exc:
    win32print = None
    print(f"[WARN] pywin32/win32print not available: {exc}")


def raw_print(printer_name: str, data: bytes, job_name: str = "Bravo POS Raw Print") -> bool:
    if not data:
        logger.error("raw_print called with empty data. job=%s", job_name)
        return False

    if win32print is None:
        logger.error("win32print is not available. Cannot print. job=%s", job_name)
        return False

    printer_handle = None
    try:
        printer_handle = win32print.OpenPrinter(printer_name)
        job_id = win32print.StartDocPrinter(printer_handle, 1, (job_name, None, "RAW"))
        try:
            win32print.StartPagePrinter(printer_handle)
            win32print.WritePrinter(printer_handle, data)
            win32print.EndPagePrinter(printer_handle)
        finally:
            win32print.EndDocPrinter(printer_handle)

        logger.info("Printed successfully. printer=%s job_id=%s bytes=%s", printer_name, job_id, len(data))
        return True
    except Exception as exc:
        logger.exception("Printing failed on printer %s: %s", printer_name, exc)
        return False
    finally:
        if printer_handle is not None:
            try:
                win32print.ClosePrinter(printer_handle)
            except Exception:
                pass
