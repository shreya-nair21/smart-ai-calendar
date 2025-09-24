import requests

BASE_URL = "http://127.0.0.1:5000"

tasks = [
    {"task": "Study", "duration": 2},
    {"task": "Gym", "duration": 1},
    {"task": "Meditation", "duration": 1}
]

res2 = requests.post(f"{BASE_URL}/schedule", json={"tasks": tasks})

print("Status code:", res2.status_code)
print("Raw response:", res2.text)

try:
    print("JSON response:", res2.json())
except Exception as e:
    print("JSON decode failed:", e)
