import json
from os.path import exists

user_file = "users.json"

def load_users():
  if exists(user_file):
    with open(user_file, "r") as f:
      return json.load(f)
    return {}
  

def save_users(users):
  with open(user_file, "w") as f:
    json.dump(users, f, indent=4)


def register_user(username, password):
  users = load_users()
  if username in users:
    return {"error" : "username already exists"}
  users[username] = {"password" : password}
  save_users(users)
  return {"message" : f"User {username} registered successfully"}

def login_user(username, password):
  users = load_users()
  if username not in users:
    return {"error" : "username not found"}
  if users[username]["password"] != password:
    return {"error" : "Invalid password"}
  return {"message" : f"User {username} logged in successfully"}