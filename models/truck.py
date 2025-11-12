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
	
