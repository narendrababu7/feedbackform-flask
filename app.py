from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

DB_NAME = "feedback.db"

# Ensure database and table exist
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedbacks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT NOT NULL,
            email TEXT NOT NULL,
            comments TEXT NOT NULL,
            submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Get database connection
def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

# Initialize database on first run
if not os.path.exists(DB_NAME):
    init_db()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/feedback', methods=["GET", "POST"])
def feedback():
    if request.method == "POST":
        student_name = request.form["student_name"]
        email = request.form["email"]
        comments = request.form["comments"]

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO feedbacks (student_name, email, comments) VALUES (?, ?, ?)",
            (student_name, email, comments)
        )
        conn.commit()
        conn.close()

        return redirect("/")
    return render_template("feedback.html")

@app.route('/admin')
def admin():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM feedbacks ORDER BY submitted_at DESC")
    feedbacks = cursor.fetchall()
    conn.close()
    return render_template("admin.html", feedbacks=feedbacks)

if __name__ == "__main__":
    app.run(debug=True)
