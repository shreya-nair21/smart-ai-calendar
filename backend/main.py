#contains logic: tasks, habits, schedule

import dateparser
from datetime import datetime, timedelta
import json
from os.path import exists

habits_file = "habits.json"
schedule_file = "schedule.json"

#parser

def parse_task(task_str):
    tokens = task_str.split(" from ")
    if len(tokens) != 2:
        return {"error": "invalid format"}
    
    task_name = tokens[0].strip()
    time_range = tokens[1].strip()
    
    start_time = dateparser.parse(time_range.split(" to ")[0])
    end_time = dateparser.parse(time_range.split(" to ")[1])
    
    return {
        "task": task_name,
        "start": start_time.strftime("%H:%M"),
        "end": end_time.strftime("%H:%M")
    }

#Habit tracker 

def load_habits():
    if exists(habits_file):
        with open(habits_file,"r") as f:
            return json.load(f)
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
    return max(habits[task_name], key=habits[task_name].get)

# Smart Scheduler

def load_schedule():
    if exists(schedule_file):
        with open(schedule_file, "r") as f:
            return json.load(f)
    return []

def save_schedule(schedule):
    with open(schedule_file, "w") as f:
        json.dump(schedule, f, indent=4)

def smart_schedule(tasks, start_hour=9):
    schedule = []
    occupied_hours = set()
    current_time = datetime.now().replace(hour=start_hour, minute=0, second=0, microsecond=0)


    for task in tasks:
        task_name = task.get("task")
        if not task_name:
            continue
        duration = float(task.get("duration", 1))
        
        preferred_hour = get_preferred_hour(task_name)
        if preferred_hour is not None:
            task_start_hour = int(preferred_hour)
        else:
            task_start_hour = current_time.hour
        
        while any(h in occupied_hours for h in range(task_start_hour, task_start_hour + int(duration))):
            task_start_hour += 1
            if task_start_hour > 23:
                task_start_hour = 0
        
        task_start = current_time.replace(hour=task_start_hour, minute=0)
        task_end = task_start + timedelta(hours=duration)
        
        for h in range(task_start_hour, task_start_hour + int(duration)):
            occupied_hours.add(h % 24)
        
        schedule.append({
            "task": task_name,
            "start": task_start.strftime("%H:%M"),
            "end": task_end.strftime("%H:%M")
        })
        
        update_habits(task_name, task_start_hour)
        current_time = task_end + timedelta(minutes=30)
    
    return schedule
