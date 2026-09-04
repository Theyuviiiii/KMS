# KMS Recruitment Website

Multi-step recruitment portal for KIET Movie Society (KMS), with protected admin access, dark mode, full application details, and a Google Sheets shortcut.

## Local run
```bash
pip install -r requirements.txt
python app.py
```
Open `http://127.0.0.1:5000/`.

## Admin
Open `/admin`. It redirects to `/admin/login` until authenticated.

Default credentials (override in production):
- Username: `Yuvraj8707`
- Password: `Yuvraj8707`

## Google Sheet button
Set the Vercel environment variable `GOOGLE_SHEET_URL` to your actual Google Sheet URL. The **Open Google Sheet ↗** button in Applications will open it in a new tab.

The button is a shortcut to the sheet; automatic form-to-Sheets syncing requires Google Sheets API/service-account configuration separately.

## Vercel environment variables
Recommended:
- `FLASK_SECRET_KEY` — long random secret
- `ADMIN_USERNAME`
- `ADMIN_PASSWORD`
- `GOOGLE_SHEET_URL`

SQLite is retained for simple/local use. For production-scale persistent submissions on Vercel, use a managed database or Google Sheets/API storage.
