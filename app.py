from flask import Flask, jsonify
import psycopg2
import os

app = Flask(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL")
conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

# 🔹 GET toutes les tâches
@app.route("/tasks", methods=["GET"])
def get_tasks():
    cur.execute("SELECT * FROM tasks")
    rows = cur.fetchall()
    return jsonify([{"id": r[0], "title": r[1]} for r in rows])

# 🔹 AJOUT via URL (POST)
@app.route("/tasks/add/<title>", methods=["POST"])
def add_task(title):
    cur.execute(
        "INSERT INTO tasks (title) VALUES (%s) RETURNING id",
        (title,)
    )
    new_id = cur.fetchone()[0]
    conn.commit()

    return jsonify({"id": new_id, "title": title})

# 🔹 MODIFIER via URL (PUT)
@app.route("/tasks/update/<int:id>/<title>", methods=["PUT"])
def update_task(id, title):
    cur.execute(
        "UPDATE tasks SET title=%s WHERE id=%s",
        (title, id)
    )
    conn.commit()

    return jsonify({"id": id, "title": title})

# 🔹 DELETE
@app.route("/tasks/delete/<int:id>", methods=["DELETE"])
def delete_task(id):
    cur.execute("DELETE FROM tasks WHERE id=%s", (id,))
    conn.commit()

    return "Deleted"

app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 3000)))
