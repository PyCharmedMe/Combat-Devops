from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

DB_PATH = "/data/scores.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS scores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        player TEXT,
        score INTEGER
    )
    """)

    conn.commit()
    conn.close()

@app.route("/")
def index():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT player, score FROM scores ORDER BY score DESC")
    scores = cursor.fetchall()

    conn.close()

    return render_template("index.html", scores=scores)

@app.route("/add", methods=["POST"])
def add_score():
    player = request.form["player"]
    score = request.form["score"]

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO scores (player, score) VALUES (?, ?)",
        (player, score)
    )

    conn.commit()
    conn.close()

    return redirect("/")

if __name__ == "__main__":
    os.makedirs("/data", exist_ok=True)
    init_db()

    app.run(host="0.0.0.0", port=5000)