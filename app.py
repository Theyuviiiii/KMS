from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from functools import wraps
import sqlite3
import os
import json
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "change-this-in-vercel")
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=os.environ.get("VERCEL", "").lower() == "1",
)

ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "Yuvraj8707")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "Yuvraj8707")

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("admin_logged_in"):
            return redirect(url_for("admin_login"))
        return f(*args, **kwargs)
    return decorated_function
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database", "kms_recruitment.db")

DOMAINS = [
    "Acting", "Direction", "Cinematography", "Editing",
    "Writing", "Social Media", "Event Management"
]

def get_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            roll_no TEXT NOT NULL,
            branch TEXT NOT NULL,
            year TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            domain TEXT NOT NULL,
            reason TEXT NOT NULL,
            experience TEXT,
            portfolio TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

@app.route("/")
def index():
    return render_template("index.html", domains=DOMAINS)

@app.post("/apply")
def apply():
    data = request.form
    required = ["name", "roll_no", "branch", "year", "email", "phone", "domain", "reason"]
    if any(not data.get(field, "").strip() for field in required):
        return jsonify({"ok": False, "message": "Please fill all required fields."}), 400

    if data["domain"] not in DOMAINS:
        return jsonify({"ok": False, "message": "Please select a valid KMS domain."}), 400

    db_saved = False
    try:
        conn = get_db()
        conn.execute("""
            INSERT INTO applications
            (name, roll_no, branch, year, email, phone, domain, reason, experience, portfolio)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data["name"].strip(), data["roll_no"].strip(), data["branch"].strip(),
            data["year"].strip(), data["email"].strip(), data["phone"].strip(),
            data["domain"].strip(), data["reason"].strip(),
            data.get("experience", "").strip(), data.get("portfolio", "").strip()
        ))
        conn.commit()
        conn.close()
        db_saved = True
    except Exception as exc:
        # Vercel's serverless filesystem may be read-only. Google Sheets is the
        # durable store when the Apps Script URL is configured.
        app.logger.warning("SQLite save skipped: %s", exc)

    # Mirror the complete application to Google Sheets when an Apps Script
    # web-app endpoint is configured. The local DB remains the admin fallback.
    sheet_saved = False
    sheet_url = os.environ.get("GOOGLE_APPS_SCRIPT_URL", "").strip()
    if sheet_url:
        payload = {
            "name": data["name"].strip(),
            "roll_no": data["roll_no"].strip(),
            "branch": data["branch"].strip(),
            "year": data["year"].strip(),
            "email": data["email"].strip(),
            "phone": data["phone"].strip(),
            "domain": data["domain"].strip(),
            "reason": data["reason"].strip(),
            "experience": data.get("experience", "").strip(),
            "portfolio": data.get("portfolio", "").strip(),
        }
        try:
            body = json.dumps(payload).encode("utf-8")
            req = Request(sheet_url, data=body, headers={"Content-Type": "application/json"}, method="POST")
            with urlopen(req, timeout=8) as response:
                if response.status >= 400:
                    raise RuntimeError(f"Google Sheets endpoint returned {response.status}")
        except (URLError, HTTPError, RuntimeError, TimeoutError) as exc:
            # Do not reject the applicant if the external sheet is temporarily down.
            app.logger.warning("Google Sheets sync failed: %s", exc)

    if not db_saved and not sheet_saved:
        return jsonify({"ok": False, "message": "We could not save your application right now. Please try again in a moment."}), 500

    return jsonify({"ok": True, "message": "Application submitted successfully!"})

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["admin_logged_in"] = True
            return redirect(url_for("admin"))
        error = "Invalid username or password."
    return render_template("admin_login.html", error=error)

@app.route("/admin/logout")
def admin_logout():
    session.clear()
    return redirect(url_for("admin_login"))

@app.route("/admin")
@admin_required
def admin():
    conn = get_db()
    applications = conn.execute(
        "SELECT * FROM applications ORDER BY id DESC"
    ).fetchall()
    conn.close()
    google_sheet_url = os.environ.get("GOOGLE_SHEET_URL", "https://docs.google.com/spreadsheets/d/1QTdTy3Va6bKMeYTg9DQw7-mF-QX5NgBiT6RgvpPehpU/edit?usp=sharing")
    return render_template("admin.html", applications=applications, google_sheet_url=google_sheet_url)

init_db()

if __name__ == "__main__":
    app.run(debug=True)
