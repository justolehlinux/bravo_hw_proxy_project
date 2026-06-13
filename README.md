# Bravo Hardware Proxy v0.3.0

FastAPI replacement for Odoo POS Windows Virtual IoT / hardware proxy.

## What it does

- Listens on port `9123`.
- Handles Odoo POS calls:
  - `GET /`
  - `GET /hw_proxy/hello`
  - `OPTIONS/POST/GET /hw_proxy/status_json`
  - `OPTIONS/POST/GET /hw_proxy/handshake`
  - `OPTIONS/POST /hw_proxy/default_printer_action`
- Handles tests:
  - `POST /test/print`
  - `POST /test/cashbox`
  - `GET /test/scale`
- For `action: cashbox`, sends multiple common ESC/POS drawer pulses to `POS58ENG`.
- For `action: print_receipt`, decodes Odoo's base64 JPEG receipt and prints it as ESC/POS raster image.
- Reads scale from `COM3`, `9600 8N1`, timeout `1`.
- Logs every default printer payload to `logs/default_printer_action_*.json` and `logs/last_default_printer_action.json`.
- Does not crash on printer/COM errors.

## Install

```powershell
git clone https://github.com/justolehlinux/bravo_hw_proxy_project

cd bravo_hw_proxy_project

python3.14.exe -m venv .venv
.\.venv\Scripts\activate

pip install -r requirements.txt
```

## Run

```powershell
.venv/Scripts/python.exe .\run.py
```

## Odoo POS IoT address

```text
192.168.18.141:9123
```

## Test

```powershell
curl http://127.0.0.1:9123/
curl http://127.0.0.1:9123/hw_proxy/hello
curl -X POST http://127.0.0.1:9123/test/print
curl -X POST http://127.0.0.1:9123/test/cashbox
curl http://127.0.0.1:9123/test/scale
```

## Receipt tuning

Edit `bravo_hw_proxy/core/config.py`:

```python
PRINTER_DOTS_WIDTH = 384
RECEIPT_THRESHOLD = 180
RECEIPT_CROP_PADDING = 8
RECEIPT_ROTATE_90 = False
```

For 58mm printers, `384` is usually correct.

If the receipt is too dark, lower `RECEIPT_THRESHOLD` to `160`.
If the receipt is too light, raise it to `200`.
If the receipt is sideways, set `RECEIPT_ROTATE_90 = True`.

## Cashbox troubleshooting

If `/test/cashbox` prints no paper and returns success, the pulse was sent to the printer spooler.
If the drawer does not physically open:

1. Make sure the cash drawer is connected to the printer's `DK` / `Cash Drawer` RJ11/RJ12 port, not to the PC.
2. Check that the cable is the correct cash-drawer cable, not a phone cable.
3. Check printer driver/tool utility for cash drawer support.
4. Try another drawer/printer combo if possible.
