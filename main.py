#Natural language task parser: 
import dateparser
from datetime import datetime, timedelta

def parse_task(task_str):
  tokens = task_str.split(" from ")

  if len(tokens) != 2:
    return{"error" : "invalid format"}
  
  task_name = tokens[0].strip()
  time_range = tokens[1].strip()

  start_time = dateparser.parse(time_range.split(" to ")[0])
  end_time = dateparser.parse(time_range.split(" to ")[1])

  return{
    "task": task_name,
    "start": start_time.strftime("%H:%M"),
    "end": end_time.strftime("%H:%M")

  }



# Habit tracker

import json
from collections import defaultdict
from os.path import exists

habits_file = "habits.json"  #stores user's habits

def load_habits():
  if exists(habits_file):
    with open(habits_file,"r") as f:
      return json.load(f)
  return {}

def save_habits(habits):
  with open(habits_file, "w")as f:
    json.dump(habits, f , indent=4)


def update_habits(task_name , hour):
  habits = load_habits()
  if task_name not in habits:
    habits[task_name] = {}  #creates new entry
  if str(hour) not in habits[task_name]:
    habits[task_name][str(hour)] = 0 #if current hour has not been used then initialize to 0
  habits[task_name][str(hour)] += 1
  save_habits(habits)


def get_preferred_hour(task_name):
  habits = load_habits()
  if task_name not in habits:
    return None
  hour_counts = habits[task_name]
  return max(hour_counts , key=hour_counts.get)





#Smart scheduler

from datetime import datetime, timedelta

def smart_schedule(tasks , start_hour=9):
  schedule = []
  current_time = datetime.now().replace(hour=start_hour, minute=0, second=0, microsecond=0)
  
  for task in tasks:
    duration = task.get("duration" , 1)
    task_start = current_time
    task_end = current_time + timedelta(hours=duration)


    schedule.append({
      "task": task["task"],
      "start": task_start.strftime("%H:%M"),
      "end": task_end.strftime("%H:%M")
    })

    current_time = task_end + timedelta(minutes=30) #30 min break

  return schedule

task_list = [
    {"task": "Study", "duration": 2},
    {"task": "Gym", "duration": 1}
]

print(smart_schedule(task_list, start_hour=10))


  










