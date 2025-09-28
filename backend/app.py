#contains Flask entrypoint

from flask import Flask, request, jsonify,send_from_directory
from backend.main import parse_task, update_habits, smart_schedule, load_habits, save_schedule, load_schedule
from backend.auth import register_user, login_user

app = Flask(__name__)

#Home
@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

#Auth

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"error": "username and password required"}), 400
    result = register_user(username, password)
    return jsonify(result)

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"error": "username and password required"}), 400
    result = login_user(username, password)
    return jsonify(result)


#Tasks

@app.route("/parse-task", methods=["POST"])
def parse():
    data = request.get_json(silent=True) or {}
    task_input = data.get("task_input")
    if not task_input:
        return jsonify({"error": "task_input is required"}), 400

    parsed = parse_task(task_input)
    if "error" in parsed:
        return jsonify({"error": parsed["error"]}), 400

    # Track the hour the user gave
    try:
        hour = int(parsed["start"].split(":")[0])
        update_habits(parsed["task"], hour)
    except Exception as e:
        print("Habit update failed:", e)

    return jsonify(parsed)

@app.route("/schedule", methods=["POST"])
def schedule():
    data = request.get_json(silent=True) or {}
    tasks = data.get("tasks", [])
    if not isinstance(tasks, list):
        return jsonify({"error": "tasks must be a list"}), 400

    result = smart_schedule(tasks)
    return jsonify(result)

@app.route("/get-schedule", methods=["GET"])
def get_schedule():
    return jsonify(load_schedule())

@app.route("/delete-task", methods=["POST"])
def delete_task():
    data = request.get_json(silent=True) or {}
    task_name = data.get("task")
    schedule = load_schedule()
    schedule = [t for t in schedule if t["task"] != task_name]
    save_schedule(schedule)
    return jsonify({"message": f"Task '{task_name}' deleted", "schedule" : schedule})

#Habits
@app.route("/habits", methods=["GET"])
def habits():
    return jsonify(load_habits())

if __name__ == "__main__":
    app.run(debug=True)
