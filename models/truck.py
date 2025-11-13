class Truck:

	"""	
	Represents a truck in the fleet
	Each truck has identifying details and can be linked to batteries
	"""

	def __init__(self, truck_id: int, VIN: str, make: str, model: str, year: int):
		"""	
		Constructor for truck data
		Args:
			truck_id (int): Unique ID for the truck
			VIN (str): VIN of the truck
			make (str): make of the truck
			model (str): model of the truck
			year (int): manufacture year of the truck 
		"""

		self._truck_id = truck_id
		self.VIN = VIN
		self.make = make
		self.model = model
		self.year = year

		self._batteries = []
		self._telemetry = []


	# ===== Getter Methods =====


	@property
	def truck_id(self) -> int:
		return self._truck_id

	@property
	def VIN(self) -> str:
		return self._VIN
	
	@property
	def make(self) -> str:
		return self._make

	@property
	def model(self) -> str:
		return self._model

	@property
	def year(self) -> int:
		return self._year
	
	@property
	def batteries(self) -> list:
		return self._batteries
	
	@property
	def telemetry(self) -> list:
		return self._telemetry
	

	# ===== Setter Methods =====

	@VIN.setter
	def VIN(self, new_VIN: str):
		"""Set and normalize the truck's VIN (always uppercase)"""

		if not new_VIN or len(new_VIN.strip()) < 5:
			raise ValueError("VIN must be at least 5 characters long.")
		self._VIN = new_VIN.strip().upper()

	@make.setter
	def make(self, new_make: str):
		"""Set and normalize the truck's make (capitalize)"""

		if not new_make:
			raise ValueError("Make cannot be empty.")
		if not isinstance(new_make, str):
			raise ValueError("Invalid make")
		self._make = new_make.strip().title()

	@model.setter
	def model(self, new_model: str):
		"""Set and normalize the truck's model (capitalize)"""

		if not new_model:
			raise ValueError("Model cannot be empty")
		if not isinstance(new_model, str):
			raise ValueError("Invalid model")
		self._model = new_model.strip().title()

	@year.setter
	def year(self, new_year: int):
		"""Set and validate the truck's manufacture year"""

		year_str = str(new_year)
		if not isinstance(new_year, int) or len(year_str) != 4 or new_year > 2030:
			raise ValueError("Year must be a valid manufacture year")
		self._year = new_year


	# ===== Methods =====

	def add_battery(self, battery):
		"""
		Link a Battery object to this truck
		"""
		self._batteries.append(battery)

	def add_telemetry(self, record):
		self._telemetry.append(record)

	def __str__(self) -> str:
		"""Return string representation of the truck"""
		return f"Truck({self._truck_id}): {self._make} {self._model} ({self._year}) - VIN: {self._VIN}"