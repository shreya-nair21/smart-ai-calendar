from flask import Flask, request, jsonify
from main import parse_task, update_habits, smart_schedule
from flask import send_from_directory
app = Flask(__name__)

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')




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

if __name__ == "__main__":
    app.run(debug=True)
