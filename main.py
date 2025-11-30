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
from services.analytics_engine import AnalyticsEngine

from datetime import datetime

def pause():
    input("\nPress ENTER to continue...")


# ============================================================
# USER MANAGEMENT
# ============================================================

def login(users):
    print("\n--- Login ---")
    email = input("Enter your email: ").strip().lower()

    user = next((u for u in users if u.email == email), None)

    if not user:
        print("User not found.")
        return None
    
    password = input("Enter your password: ")

    if not user.check_password(password):
        print("Incorrect password.")
        return None

    print(f"Welcome {user.name}!")
    return user


def add_user(users):
    print("\n--- Add New User ---")
    try:
        user_id = int(input("Enter User ID: "))
        name = input("Enter name: ")
        email = input("Enter email: ")

        # ===== CHECK FOR EXISTING EMAIL IN JSON =====
        if any(u.email == email for u in users):
            print("Error: A user with this email already exists")
            pause()
            return
        
        password = input("Enter password: ")
        role = input("Enter role (manager/admin/etc): ")

        new_user = User(user_id, name, email, password, role)
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

def confirm_admin(user):
    if not user.is_admin():
        print("Access denied: Admin only.")
        return False
    return True


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

def delete_truck(current_user, trucks, batteries, telemetry):
    print("\n--- Delete Truck ---")

    # Admin permission check
    if not confirm_admin(current_user):
        return
    
    truck_id = int(input("Enter Truck ID to delete: "))

    truck = next((t for t in trucks if t.truck_id == truck_id), None)

    if not truck:
        print("Truck not found.")
        pause()
        return
    
    # Remove batteries that belong to this struck
    batteries[:] = [b for b in batteries if b.truck.truck_id != truck_id]

    # Remove telemetry data for this truck
    telemetry[:] = [tr for tr in telemetry if tr.truck.truck_id != truck_id]
    
    # Remove the truck itself
    trucks.remove(truck)

    # Save updated data
    save_trucks(trucks)
    save_batteries(batteries)
    save_telemetry(telemetry)

    print(f"Truck {truck_id} and all related batteries/telemetry deleted.")
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

def delete_battery(current_user, batteries, telemetry):
    print("\n--- Delete Battery ---")

    # Admin permission check
    if not confirm_admin(current_user):
        return

    battery_id = int(input("Battery ID: "))

    battery = next((b for b in batteries if b.battery_id == battery_id), None)

    if not battery:
        print("Battery not found.")
        pause()
        return

    telemetry[:] = [tr for tr in telemetry if tr.battery.battery_id != battery_id]

    # Remove battery
    batteries.remove(battery)

    save_batteries(batteries)
    save_telemetry(telemetry)

    print("Battery deleted.")
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

def delete_telemetry(current_user, telemetry):
    print("\n--- Delete Telemetry Record ---")

    # Admin permission check
    if not confirm_admin(current_user):
        return

    record_id = int(input("Enter Record ID: "))

    record = next((r for r in telemetry if r.record_id == record_id), None)

    if not record:
        print("Record not found.")
        pause()
        return

    telemetry.remove(record)
    save_telemetry(telemetry)

    print("Telemetry record deleted.")
    pause()

# ============================================================
# ANALYTICS MANAGEMENT
# ============================================================

def run_analytics(batteries):
    print("\n=== Battery Analytics ===")

    engine = AnalyticsEngine()

    if not batteries:
        print("No batteries in the system.")
        pause()
        return
    
    for b in batteries:
        print(engine.analyze_battery(b))
        print("--------------------------------")

    pause()

# ============================================================
# DISPLAY MENU FUNCTIONS
# ============================================================

def users_menu(users):
    while True:
        print("\n--- User Menu ---")
        print("1. Add User")
        print("2. View Users")
        print("3. Back")
        sub = input("Choose: ")

        if sub == "1":
            add_user(users)
        elif sub == "2":
            view_users(users)
        else:
            return
        
def trucks_menu(current_user, trucks, batteries, telemetry):
    while True:
        print("\n--- Truck Menu ---")
        print("1. Add Truck")
        print("2. View Trucks")
        print("3. Delete Truck (Admin Only)")
        print("4. Back")
        sub = input("Choose: ")

        if sub == "1":
            add_truck(trucks)
        elif sub == "2":
            view_trucks(trucks)
        elif sub == "3":
            delete_truck(current_user, trucks, batteries, telemetry)
        else:
            return
        
def battery_menu(current_user, trucks, batteries, telemetry):
    while True:
        print("\n--- Battery Menu ---")
        print("1. Add Battery")
        print("2. View Batteries")
        print("3. Delete Battery (Admin Only)")
        print("4. Back")
        sub = input("Choose: ")

        if sub == "1":
            add_battery(batteries, trucks)
        elif sub == "2":
            view_batteries(batteries)
        elif sub == "3":
            delete_battery(current_user, batteries, telemetry)
        else:
            return

def telemetry_menu(current_user, trucks, batteries, telemetry):
    while True:
        print("\n--- Telemetry Menu ---")
        print("1. Add Telemetry Record")
        print("2. View Telemetry")
        print("3. Delete Telemetry (Admin Only)")
        print("4. Back")
        sub = input("Choose: ")

        if sub == "1":
            add_telemetry(trucks, batteries, telemetry)
        elif sub == "2":
            view_telemetry(telemetry)
        elif sub == "3":
            delete_telemetry(current_user, telemetry)
        else:
            return

# ============================================================
# MAIN MENU
# ============================================================

def main():
    # Load everything from JSON database
    users, trucks, batteries, telemetry = load_all()

    current_user = login(users)

    if not current_user:
        print("Exiting...")
        return

    while True:
        print("\n==============================")
        print("     Fleet Management System ")
        print("==============================")
        print("1. Manage Users")
        print("2. Manage Trucks")
        print("3. Manage Batteries")
        print("4. Manage Telemetry")
        print("5. Run Analytics")
        print("6. Quit")

        choice = input("Choose an option: ")

        if choice == "1":
            users_menu(current_user, users, trucks, batteries, telemetry)

        elif choice == "2":
            trucks_menu(current_user, trucks, batteries, telemetry)

        elif choice == "3":
            battery_menu(current_user, trucks, batteries, telemetry)

        elif choice == "4":
            telemetry_menu(current_user, trucks, batteries, telemetry)

        elif choice == "5":
            run_analytics(batteries)

        elif choice == "6":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
