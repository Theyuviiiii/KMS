from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
import os

app = Flask(__name__)
DB_PATH = os.path.join("database", "kms_recruitment.db")

DOMAINS = [
    "Acting", "Direction", "Cinematography", "Editing",
    "Writing", "Social Media", "Event Management"
]

def get_db():
    os.makedirs("database", exist_ok=True)
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

    return jsonify({"ok": True, "message": "Application submitted successfully!"})

@app.route("/admin")
def admin():
    conn = get_db()
    applications = conn.execute(
        "SELECT * FROM applications ORDER BY id DESC"
    ).fetchall()
    conn.close()
    return render_template("admin.html", applications=applications)

if __name__ == "__main__":
    init_db()
    app.run(host="127.0.0.1", port=8000, debug=True)