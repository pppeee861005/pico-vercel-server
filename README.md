# Pico Vercel Server

A small Flask service for testing connectivity between a Raspberry Pi Pico 2 W, a phone, and a Vercel deployment.

## Endpoints

- `GET /` — browser test page
- `GET /api/ping` — JSON connectivity response

## Local development

```powershell
python -m pip install -r requirements.txt
python server.py
```

Deploy this directory as the Vercel project root.
