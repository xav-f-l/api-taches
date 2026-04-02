from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

# 🔗 Connexion DB
DATABASE_URL = os.environ.get("DATABASE_URL")

conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

# 🔹 créer table
cur.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL
)
""")
conn.commit()

@app.route("/")
def home():
    return "API + DB OK"

# 🔹 GET
@app.route("/tasks", methods=["GET"])
def get_tasks():
    cur.execute("SELECT * FROM tasks")
    rows = cur.fetchall()
    return jsonify([{"id": r[0], "title": r[1]} for r in rows])

# 🔹 POST
@app.route("/tasks", methods=["POST"])
def add_task():
    title = request.json["title"]

    cur.execute(
        "INSERT INTO tasks (title) VALUES (%s) RETURNING id",
        (title,)
    )
    new_id = cur.fetchone()[0]
    conn.commit()

    return jsonify({"id": new_id, "title": title})

# 🔹 PUT
@app.route("/tasks/<int:id>", methods=["PUT"])
def update_task(id):
    title = request.json["title"]

    cur.execute(
        "UPDATE tasks SET title=%s WHERE id=%s",
        (title, id)
    )
    conn.commit()

    return jsonify({"id": id, "title": title})

# 🔹 DELETE
@app.route("/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):
    cur.execute("DELETE FROM tasks WHERE id=%s", (id,))
    conn.commit()

    return "Deleted"

app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 3000)))
