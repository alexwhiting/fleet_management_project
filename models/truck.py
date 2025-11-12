class Truck:

	"""	
	Represents a truck in the fleet
	Each truck has identifying details and can be linked to batteries
	"""

	def __init__(self, truck_ID: int, VIN: str, make: str, model: str, year: int):
		"""	
		Constructor for truck data
		"""

		self._truck_ID = truck_ID
		self._VIN = VIN
		self._make = make
		self._model = model
		self._year = year
		self._batteries = []


	# ===== Getter Methods =====


	@property
	def truck_ID(self) -> int:
		"""Return the truck's ID"""
		return self._truck_ID

	@property
	def VIN(self) -> str:
		"""Return the truck's VIN"""
		return self._VIN
	
	@property
	def make(self) -> str:
		"""Return the truck's make"""
		return self._make

	@property
	def model(self) -> str:
		"""Return the truck's model"""
		return self._model

	@property
	def year(self) -> int:
		"""Return the truck's production year"""
		return self._year
	
	@property
	def batteries(self) -> list:
		"""Return a list of Battery objects linked to this truck"""
		return self._batteres
	

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
		self._make = new_model.strip().title()

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
		Args:
			battery: A Battery instance
		"""
		self._batteries.append(battery)

	def __str__(self) -> str:
		"""Return string representation of the truck"""
		return f"Truck({self._truck_ID}): {self._make} {self._model} ({self._year}) - VIN: {self._VIN}"