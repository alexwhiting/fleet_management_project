class Battery:
    """
    Represents a battery installed in a truck within the fleet system.
    Handles capacity, voltage, operational status, and linkage to its truck.
    """

    def __init__(self, battery_id: int, truck, capacity_ah: float, voltage_v: float, status: str):
        """
        Constructor for the Battery class.

        Args:
            battery_id (int): Unique ID for this battery.
            truck (Truck): The Truck object this battery belongs to.
            capacity_ah (float): Battery capacity in amp-hours.
            voltage_v (float): Battery voltage in volts
            status (str): Operational status
        """
        self._battery_id = battery_id
        self.truck = truck              
        self.capacity_ah = capacity_ah  
        self.voltage_v = voltage_v     
        self.status = status            

        # Link this battery to the truck’s list of batteries
        if truck is not None:
            truck.add_battery(self)


    # ===== Getter Methods =====


    @property
    def battery_id(self) -> int:
        return self._battery_id

    @property
    def truck(self):
        return self._truck

    @property
    def capacity_ah(self) -> float:
        return self._capacity_ah

    @property
    def voltage_v(self) -> float:
        return self._voltage_v

    @property
    def status(self) -> str:
        return self._status
    

    # ===== Setters =====


    @truck.setter
    def truck(self, new_truck):
        """Assign the battery to a truck."""
        self._truck = new_truck

    @capacity_ah.setter
    def capacity_ah(self, new_capacity: float):
        """Validate and set battery capacity."""
        if new_capacity <= 0:
            raise ValueError("Capacity must be greater than 0 Ah.")
        self._capacity_ah = float(new_capacity)

    @voltage_v.setter
    def voltage_v(self, new_voltage: float):
        """Validate and set battery voltage."""
        if new_voltage < 6 or new_voltage > 1000:
            raise ValueError("Voltage must be between 6V and 1000V.")
        self._voltage_v = float(new_voltage)

    @status.setter
    def status(self, new_status: str):
        """Set and validate operational status."""
        valid = ["active", "charging", "faulty", "idle", "depleted"]
        new_status = new_status.strip().lower()

        if new_status not in valid:
            raise ValueError(f"Invalid status. Must be one of: {', '.join(valid)}")
        self._status = new_status


    # ========= Helper Methods =========


    def is_operational(self) -> bool:
        """Return True if the battery is usable."""
        return self._status in ["active", "charging"]

    def __str__(self) -> str:
        """Readable representation of the battery."""
        truck_id = self._truck.truck_id if self._truck else "None"
        return (
            f"Battery({self._battery_id}): {self._capacity_ah}Ah, "
            f"{self._voltage_v}V, Status: {self._status.capitalize()}, "
            f"Truck ID: {truck_id}"
        )
