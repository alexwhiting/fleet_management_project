from database_manager import (
    load_all,
    save_users,
    save_trucks,
    save_batteries,
    save_telemetry
)

from models.user import User
from models.truck import Truck
from models.battery import Battery
from models.telemetry import TelemetryRecord

from datetime import datetime


# ============================================================
# UTILITY HELPERS
# ============================================================

def pause():
    input("\nPress ENTER to continue...")


# ============================================================
# USER MANAGEMENT
# ============================================================

def add_user(users):
    print("\n--- Add New User ---")
    try:
        user_id = int(input("Enter User ID: "))
        name = input("Enter name: ")
        email = input("Enter email: ")
        role = input("Enter role (manager/admin/etc): ")

        new_user = User(user_id, name, email, role)
        users.append(new_user)

        save_users(users)
        print(f"User '{new_user.name}' added successfully.")

    except ValueError as e:
        print(f"Error: {e}")

    pause()


def view_users(users):
    print("\n--- User List ---")

    if not users:
        print("No users found.")
    else:
        for u in users:
            print(u)

    pause()


# ============================================================
# TRUCK MANAGEMENT
# ============================================================

def add_truck(trucks):
    print("\n--- Add New Truck ---")

    try:
        truck_id = int(input("Enter Truck ID: "))
        vin = input("Enter VIN: ")
        make = input("Enter Make: ")
        model = input("Enter Model: ")
        year = int(input("Enter Manufacture Year: "))

        truck = Truck(truck_id, vin, make, model, year)
        trucks.append(truck)

        save_trucks(trucks)
        print("Truck added successfully.")

    except ValueError as e:
        print(f"Error: {e}")

    pause()


def view_trucks(trucks):
    print("\n--- Truck List ---")

    if not trucks:
        print("No trucks found.")
    else:
        for t in trucks:
            print(t)

    pause()


# ============================================================
# BATTERY MANAGEMENT
# ============================================================

def add_battery(batteries, trucks):
    print("\n--- Add New Battery ---")

    try:
        battery_id = int(input("Enter Battery ID: "))
        truck_id = int(input("Enter Truck ID for this battery: "))

        truck = next((t for t in trucks if t.truck_id == truck_id), None)
        if not truck:
            print("Truck not found.")
            pause()
            return

        capacity = float(input("Enter Capacity (Ah): "))
        voltage = float(input("Enter Voltage (V): "))
        status = input("Enter Status: ")

        battery = Battery(battery_id, truck, capacity, voltage, status)
        batteries.append(battery)

        save_batteries(batteries)
        save_trucks(trucks)

        print("Battery added successfully.")

    except ValueError as e:
        print(f"Error: {e}")

    pause()


def view_batteries(batteries):
    print("\n--- Battery List ---")

    if not batteries:
        print("No batteries found.")
    else:
        for b in batteries:
            print(b)

    pause()


# ============================================================
# TELEMETRY MANAGEMENT
# ============================================================

def add_telemetry(trucks, batteries, telemetry):
    print("\n--- Add Telemetry Record ---")

    try:
        record_id = int(input("Enter Record ID: "))
        truck_id = int(input("Truck ID: "))
        battery_id = int(input("Battery ID: "))

        truck = next((t for t in trucks if t.truck_id == truck_id), None)
        battery = next((b for b in batteries if b.battery_id == battery_id), None)

        if not truck:
            print("Truck not found.")
            pause()
            return

        if not battery:
            print("Battery not found.")
            pause()
            return

        temp = float(input("Temperature (°C): "))
        voltage = float(input("Voltage (V): "))
        current = float(input("Current (A): "))

        timestamp = datetime.now()

        record = TelemetryRecord(
            record_id,
            truck,
            battery,
            temp,
            voltage,
            current,
            timestamp
        )

        telemetry.append(record)
        truck.add_telemetry(record)
        battery.add_telemetry(record)

        save_telemetry(telemetry)
        save_trucks(trucks)
        save_batteries(batteries)

        print("Telemetry record added.")

    except ValueError as e:
        print(f"Error: {e}")

    pause()


def view_telemetry(telemetry):
    print("\n--- Telemetry Records ---")

    if not telemetry:
        print("No telemetry found.")
    else:
        for t in telemetry:
            print(t)

    pause()


# ============================================================
# MAIN MENU
# ============================================================

def main():
    # Load everything from JSON database
    users, trucks, batteries, telemetry = load_all()

    while True:
        print("\n==============================")
        print("     Fleet Management System ")
        print("==============================")
        print("1. Manage Users")
        print("2. Manage Trucks")
        print("3. Manage Batteries")
        print("4. Manage Telemetry")
        print("5. Quit")

        choice = input("Choose an option: ")

        # -------------------------
        # USERS SUBMENU
        # -------------------------
        if choice == "1":
            print("\n--- User Menu ---")
            print("1. Add User")
            print("2. View Users")
            print("3. Back")
            sub = input("Choose: ")

            if sub == "1":
                add_user(users)
            elif sub == "2":
                view_users(users)

        # -------------------------
        # TRUCK SUBMENU
        # -------------------------
        elif choice == "2":
            print("\n--- Truck Menu ---")
            print("1. Add Truck")
            print("2. View Trucks")
            print("3. Back")
            sub = input("Choose: ")

            if sub == "1":
                add_truck(trucks)
            elif sub == "2":
                view_trucks(trucks)

        # -------------------------
        # BATTERY SUBMENU
        # -------------------------
        elif choice == "3":
            print("\n--- Battery Menu ---")
            print("1. Add Battery")
            print("2. View Batteries")
            print("3. Back")
            sub = input("Choose: ")

            if sub == "1":
                add_battery(batteries, trucks)
            elif sub == "2":
                view_batteries(batteries)

        # -------------------------
        # TELEMETRY SUBMENU
        # -------------------------
        elif choice == "4":
            print("\n--- Telemetry Menu ---")
            print("1. Add Telemetry Record")
            print("2. View Telemetry")
            print("3. Back")
            sub = input("Choose: ")

            if sub == "1":
                add_telemetry(trucks, batteries, telemetry)
            elif sub == "2":
                view_telemetry(telemetry)

        # -------------------------
        # EXIT
        # -------------------------
        elif choice == "5":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
