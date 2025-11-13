# models/telemetry.py
from datetime import datetime

class TelemetryRecord:
    """
    Represents a single telemetry reading taken from a truck's sensors.
    Includes temperature, voltage, current, and timestamp.
    """

    def __init__(self, record_id: int, truck, battery,
                 temperature_c: float, voltage_v: float,
                 current_a: float, timestamp=None):
        """
        Args:
            record_id (int): Unique ID for the telemetry record.
            truck (Truck): Truck associated with this telemetry.
            battery (Battery): Battery associated with this telemetry.
            temperature_c (float): Temperature in Celsius.
            voltage_v (float): Voltage in volts.
            current_a (float): Current in amperes.
            timestamp (datetime | None): Timestamp of measurement.
        """
        self._record_id = record_id
        self.truck = truck             
        self.battery = battery         
        self.temperature_c = temperature_c
        self.voltage_v = voltage_v
        self.current_a = current_a
        self.timestamp = timestamp or datetime.now()

        # Link into truck + battery for easy referencing
        if truck is not None:
            truck.add_telemetry(self)


    # ===== Getter Methods =====


    @property
    def record_id(self):
        return self._record_id

    @property
    def truck(self):
        return self._truck

    @property
    def battery(self):
        return self._battery

    @property
    def temperature_c(self):
        return self._temperature_c

    @property
    def voltage_v(self):
        return self._voltage_v

    @property
    def current_a(self):
        return self._current_a

    @property
    def timestamp(self):
        return self._timestamp


    # ===== Setters =====


    @truck.setter
    def truck(self, new_truck):
        self._truck = new_truck

    @battery.setter
    def battery(self, new_battery):
        self._battery = new_battery

    @temperature_c.setter
    def temperature_c(self, temp):
        if temp < -40 or temp > 150:
            raise ValueError("Temperature outside valid range (-40C to 150C).")
        self._temperature_c = float(temp)

    @voltage_v.setter
    def voltage_v(self, v):
        if v < 0:
            raise ValueError("Voltage cannot be negative.")
        self._voltage_v = float(v)

    @current_a.setter
    def current_a(self, a):
        self._current_a = float(a)

    @timestamp.setter
    def timestamp(self, t):
        self._timestamp = t

    # ========= String Representation =========

    def __str__(self):
        return (f"Telemetry({self._record_id}): "
                f"{self._temperature_c}C, {self._voltage_v}V, {self._current_a}A "
                f"at {self._timestamp}")
