import json
import os
from datetime import datetime

from models.user import User
from models.truck import Truck
from models.battery import Battery
from models.telemetry import TelemetryRecord


DATA_DIR = "data"

# ===== Functions for loading and saving raw JSON =====

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


# ===== Loading functions - Converts JSON to Python Objects =====


def load_users():
    """
    Load all users from users.json and reconstruct User objects.
    Handles both new and old JSON formats.
    """
    users_raw = load_json("users.json")
    users = []

    for u in users_raw:

        if "password_hash" not in u:
            print(f"[INFO] Adding default password for user {u['email']}: 'default123'")
            
            # Create user with default password (will be hashed)
            user = User(
                u["user_id"],
                u["name"],
                u["email"],
                "default123",      
                u["role"]
            )

            users.append(user)
            continue

        user = User(
            u["user_id"],
            u["name"],
            u["email"],
            "TEMP1234",         
            u["role"]
        )

        # Override the temporary hash
        user._password_hash = u["password_hash"]

        users.append(user)

    return users




def load_trucks():
    """
    Load all trucks from trucks.json
    """
    trucks_raw = load_json("trucks.json")
    trucks = []

    for t in trucks_raw:
        truck = Truck(t["truck_id"], t["VIN"], t["make"], t["model"], 
                      t["year"])

        truck._batteries = t["batteries"]
        truck._telemetry = t["telemetry"]

        trucks.append(truck)

    return trucks


def load_batteries(trucks):
    """
    Load all batteries and link each one to its truck
    """
    batteries_raw = load_json("batteries.json")
    batteries = []

    for b in batteries_raw:
        # Find corresponding truck object
        truck = next((t for t in trucks if t.truck_id == b["truck_id"]), None)

        battery = Battery(
            b["battery_id"],
            truck,
            b["capacity_ah"],
            b["voltage_v"],
            b["status"]
        )

        battery._telemetry = b["telemetry"]

        batteries.append(battery)

    return batteries


def load_telemetry(trucks, batteries):
    """
    Load telemetry records and link them to their truck and battery.
    """
    telemetry_raw = load_json("telemetry.json")
    records = []

    for r in telemetry_raw:
        truck = next((t for t in trucks if t.truck_id == r["truck_id"]), None)
        battery = next((b for b in batteries if b.battery_id == r["battery_id"]), None)

        record = TelemetryRecord(
            r["record_id"],
            truck,
            battery,
            r["temperature_c"],
            r["voltage_v"],
            r["current_a"],
            datetime.fromisoformat(r["timestamp"])
        )

        records.append(record)

    return records


# ===== Saving functons - Convert Python Objects to JSON =====


def save_users(users):
    """
    Save all users into users.json.
    Stores SHA-256 hashed passwords.
    """
    data = []
    for u in users:
        data.append({
            "user_id": u.user_id,
            "name": u.name,
            "email": u.email,
            "role": u.role,
            "password_hash": u.password,     # already hashed
            "trucks": [t.truck_id for t in u.trucks]
        })
    save_json("users.json", data)



def save_trucks(trucks):
    """
    Save all Truck objects into trucks.json.
    Only store primitive fields + lists of IDs.
    """
    data = []
    for t in trucks:
        data.append({
            "truck_id": t.truck_id,
            "VIN": t.VIN,
            "make": t.make,
            "model": t.model,
            "year": t.year,
            "batteries": [b.battery_id for b in t.batteries],
            "telemetry": [tr.record_id for tr in t.telemetry]
        })
    save_json("trucks.json", data)


def save_batteries(batteries):
    """
    Save all Battery objects into batteries.json.
    """
    data = []
    for b in batteries:
        data.append({
            "battery_id": b.battery_id,
            "truck_id": b.truck.truck_id if b.truck else None,
            "capacity_ah": b.capacity_ah,
            "voltage_v": b.voltage_v,
            "status": b.status,
            "telemetry": [t.record_id for t in b.telemetry]
        })
    save_json("batteries.json", data)


def save_telemetry(records):
    """
    Save all telemetry records into telemetry.json.
    """
    data = []
    for r in records:
        data.append({
            "record_id": r.record_id,
            "truck_id": r.truck.truck_id if r.truck else None,
            "battery_id": r.battery.battery_id if r.battery else None,
            "temperature_c": r.temperature_c,
            "voltage_v": r.voltage_v,
            "current_a": r.current_a,
            "timestamp": r.timestamp.isoformat()
        })
    save_json("telemetry.json", data)


# ===== Master Loader =====


def load_all():
    """
    Load ALL data and rebuild full relationships:
    User -> Trucks -> Batteries -> TelemetryRecords
    """

    users = load_users()
    trucks = load_trucks()
    batteries = load_batteries(trucks)
    telemetry = load_telemetry(trucks, batteries)

    # --- Reconnect Users -> Trucks ---
    users_raw = load_json("users.json")
    for u_data, user in zip(users_raw, users):
        for truck_id in u_data["trucks"]:
            truck_obj = next((t for t in trucks if t.truck_id == truck_id), None)
            if truck_obj:
                user.add_truck(truck_obj)

    # --- Reconnect Trucks -> Batteries ---
    trucks_raw = load_json("trucks.json")
    for t_data, truck in zip(trucks_raw, trucks):
        truck._batteries = []
        for battery_id in t_data["batteries"]:
            b_obj = next((b for b in batteries if b.battery_id == battery_id), None)
            if b_obj:
                truck.add_battery(b_obj)

    # --- Reconnect Trucks -> Telemetry ---
    for t_data, truck in zip(trucks_raw, trucks):
        truck._telemetry = []
        for record_id in t_data["telemetry"]:
            r_obj = next((r for r in telemetry if r.record_id == record_id), None)
            if r_obj:
                truck.add_telemetry(r_obj)

    # --- Reconnect Batteries -> Telemetry ---
    batteries_raw = load_json("batteries.json")
    for b_data, battery in zip(batteries_raw, batteries):
        battery._telemetry = []
        for record_id in b_data["telemetry"]:
            r_obj = next((r for r in telemetry if r.record_id == record_id), None)
            if r_obj:
                battery.add_telemetry(r_obj)

    return users, trucks, batteries, telemetry