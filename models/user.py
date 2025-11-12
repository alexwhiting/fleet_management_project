class User:

	"""
	Represents a system user (e.g., fleet manager or admin)
	Handles user data, including userID, name, email, role, and assigned trucks
	"""

	def __init__(self, user_id: int, name: str, email: str, role: str):
		"""
		Constructor for the User class
		"""
		self._user_id = user_id
		self._name = name.strip().title()
		self._email = email.strip().lower()
		self._role = role.strip().lower()
		self._trucks = [] # list of Truck objects the user manages


	# ===== Getter Methods =====


	@property
	def user_ID(self) -> int:
		"""Return the user's unique ID"""
		return self._user_id
	
	@property
	def name(self) -> str:
		"""Return the user's name"""
		return self._name
	
	@property
	def email(self) -> str:
		"""Return the user's email address"""
		return self._email
	
	@property 
	def role(self) -> str:
		"""Return the user's role"""
		return self._role
	
	@property 
	def trucks(self) -> list:
		"""Return a lsit of trucks managed by this user"""
		return self._trucks
	
	
	# ===== Setter Methods =====


	@name.setter
	def name(self, new_name: str):
		"""Set and normalize the user's name"""
		if not new_name:	
			raise ValueError("Name cannot be empty")
		self._name = new_name.strip().title() # Capitalize each word

	@email.setter
	def email(self, new_email: str):
		"""Set and normalize the user's email"""
		if "@" not in new_email or "." not in new_email:
			raise ValueError("Invalid email address")
		self._email = new_email.strip().lower()

	@role.setter
	def role(self, new_role: str):
		"""Update the user's role"""
		if not new_role:
			raise ValueError("Invalid role")
		self._role = new_role.strip().lower()


	# ===== Methods =====


	def add_truck(self, truck):
		"""Assign a new Truck object to this user"""
		self._trucks.append(truck)

	def get_trucks(self) -> list:
		"""Return all trucks managed by the user"""
		return self._trucks
	
	def __str__(self) -> str:
		"""Return string representation of the user"""
		return f"User({self._user_id}): {self._name} ({self._role})"
							 