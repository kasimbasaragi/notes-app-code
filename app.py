import os
import time
import socket
from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def get_conn():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        dbname=os.getenv("DB_NAME", "notesdb"),
        user=os.getenv("DB_USER", "appuser"),
        password=os.getenv("DB_PASSWORD"),
    )


def init_db():
    """Create tables from db/init.sql. Retries while the database is starting."""
    with open(os.path.join(BASE_DIR, "db", "init.sql")) as f:
        sql = f.read()
    for _ in range(15):
        try:
            conn = get_conn()
            cur = conn.cursor()
            cur.execute(sql)
            conn.commit()
            conn.close()
            return
        except Exception:
            time.sleep(2)
    raise RuntimeError("Database not reachable")


@app.route("/health")
def health():
    return {"status": "ok", "served_by": socket.gethostname()}


@app.route("/notes", methods=["GET", "POST"])
def notes():
    conn = get_conn()
    cur = conn.cursor()
    if request.method == "POST":
        cur.execute("INSERT INTO notes (text) VALUES (%s)", (request.json["text"],))
        conn.commit()
        conn.close()
        return {"message": "saved"}, 201
    cur.execute("SELECT id, text, created_at FROM notes ORDER BY id DESC")
    rows = [{"id": r[0], "text": r[1], "created_at": str(r[2])} for r in cur.fetchall()]
    conn.close()
    return jsonify(notes=rows, served_by=socket.gethostname())


init_db()
