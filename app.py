from flask import Flask, request, jsonify
import os

app = Flask(__name__)

tasks = [
    {"id": 1, "title": "Première tâche"}
]

@app.route("/")
def home():
    return "API TACHES OK"
    
@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(tasks)

@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.get_json()

    if not data or "title" not in data:
        return jsonify({"error": "JSON invalide"}), 400

    new_task = {
        "id": len(tasks) + 1,
        "title": data["title"]
    }

    tasks.append(new_task)
    return jsonify(new_task), 201

@app.route("/tasks/<int:id>", methods=["PUT"])
def update_task(id):
    data = request.get_json()

    if not data or "title" not in data:
        return jsonify({"error": "JSON invalide"}), 400

    for task in tasks:
        if task["id"] == id:
            task["title"] = data["title"]
            return jsonify(task)

    return jsonify({"error": "Not found"}), 404

@app.route("/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):
    global tasks
    tasks = [t for t in tasks if t["id"] != id]
    return "Deleted"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 3000)))
