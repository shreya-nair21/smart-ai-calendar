from flask import Flask , request , jsonify
from main import parse_task, update_habits, smart_schedule


app = Flask(__name__)

@app("/parse-task", methods=["POST"])

def parse():
  data = request.json
  task_input = data.get("task_input")
  parsed = parse_task(task_input)
  if "error" in parsed:
    return jsonify({"error": parsed["error"]}), 400
  update_habits(parsed["task"], int(parsed["start"].split(":")[0]))
  return jsonify(parsed)



@app.route("/schedule" , metthods=["POST"])

def schedule():
  data=request.json
  tasks=data.get("tasks" , [])
  result=smart_schedule(tasks)
  return jsonify(result)

if __name__ == "__main__":
  app.run(debug=True)