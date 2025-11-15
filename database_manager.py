import json
import os
from models.user import User
from models.truck import Truck
from models.battery import Battery
from models.telemetry import TelemetryRecord
from datetime import datetime

DATA_DIR = "data"

def load_json(filename):
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        with open(path, "w") as f:
            f.write("[]")
    with open(path, "r") as f:
        return json.load(f)
    
def save_json(filename, data):
    path = os.path.join(DATA_DIR, filename)
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

def load_all():
    """
    Load all persistent data from JSON files and reconstruct full
    User, Truck, Battery, and TelemetryRecord objects with relationships
    """

    # Step 1 - Load base objects (no connections yet)
    users = load_users()

def load_users():
    """
    Load all users from users.json and reconstruct User objects
    """
    users_raw = load_json("users.json")
    users = []	

    for u in users_raw:
        user = User(u["user_id"], u["name"], u["email"], u["role"])
        users.append(user)

    return users			

def save_users(users):
    data = []
    for u in users:
        data.append({
            "user_id": u.user_id,
            "name": u.name,
            "email": u.email,
            "role": u.role,
            "trucks": [t.truck_id for t in u.trucks]
        })
    save_json("users.json", data)


