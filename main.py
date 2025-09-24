import json
from os.path import exists
from collections import defaultdict
from datetime import datetime, timedelta
import dateparser

# -------------------- Task Parser --------------------
def parse_task(task_str):
    """
    Parse a string like 'Study from 3pm to 5pm'
    Returns {task, start, end} or {"error": "..."}
    """
    if not task_str or " from " not in task_str or " to " not in task_str:
        return {"error": "Use format: 'Task name from 3pm to 5pm'"}

    try:
        task_name, time_range = task_str.split(" from ", 1)
        start_str, end_str = time_range.split(" to ", 1)

        start_time = dateparser.parse(start_str)
        end_time = dateparser.parse(end_str)

        if not start_time or not end_time:
            return {"error": "Could not parse date/time"}

        return {
            "task": task_name.strip(),
            "start": start_time.strftime("%H:%M"),
            "end": end_time.strftime("%H:%M")
        }
    except Exception:
        return {"error": "Invalid input format"}


# -------------------- Habit Tracker --------------------
habits_file = "habits.json"

def load_habits():
    if exists(habits_file):
        try:
            with open(habits_file, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    return {}

def save_habits(habits):
    with open(habits_file, "w") as f:
        json.dump(habits, f, indent=4)

def update_habits(task_name, hour):
    habits = load_habits()
    if task_name not in habits:
        habits[task_name] = {}
    if str(hour) not in habits[task_name]:
        habits[task_name][str(hour)] = 0
    habits[task_name][str(hour)] += 1
    save_habits(habits)

def get_preferred_hour(task_name):
    habits = load_habits()
    if task_name not in habits:
        return None
    hour_counts = habits[task_name]
    return max(hour_counts, key=hour_counts.get)


# -------------------- Smart Scheduler --------------------
def smart_schedule(tasks, start_hour=9):
    """
    Takes a list of {"task": "...", "duration": hours}
    Returns a list with scheduled start & end times.
    """
    schedule = []
    current_time = datetime.now().replace(hour=start_hour, minute=0, second=0, microsecond=0)

    for task in tasks:
        task_name = task.get("task")
        if not task_name:
            continue
        duration = float(task.get("duration", 1))

        task_start = current_time
        task_end = current_time + timedelta(hours=duration)

        schedule.append({
            "task": task_name,
            "start": task_start.strftime("%H:%M"),
            "end": task_end.strftime("%H:%M")
        })

        # Add 30 min break
        current_time = task_end + timedelta(minutes=30)

    return schedule


# -------------------- Quick Local Test --------------------
if __name__ == "__main__":
    print(parse_task("Study from 3pm to 5pm"))
    task_list = [
        {"task": "Study", "duration": 2},
        {"task": "Gym", "duration": 1}
    ]
    print(smart_schedule(task_list, start_hour=10))
