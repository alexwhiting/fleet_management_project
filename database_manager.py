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