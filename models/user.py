import hashlib

class User:

	"""
	Represents a system user (e.g., fleet manager or admin)
	Handles user data, including userID, name, email, password, role, and assigned trucks
	"""

	def __init__(self, user_id: int, name: str, email: str, password: str, role: str):
		"""
		Constructor for the User class
		Args:
			user_id (int): Unique ID for user
			name (str): Name of user
			email (str): Email of user
			password (str): Password of usrr
			role (str): role of user
		"""
		
		self._user_id = user_id
		self.name = name
		self.email = email
		self.password = password
		self.role = role
		self._trucks = [] 


	# ===== Getter Methods =====


	@property
	def user_id(self) -> int:
		return self._user_id
	
	@property
	def name(self) -> str:
		return self._name
	
	@property
	def email(self) -> str:
		return self._email
	
	@property
	def password(self) -> str:
		return self._password_hash
	
	@property 
	def role(self) -> str:
		return self._role
	
	@property 
	def trucks(self) -> list:
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

	@password.setter
	def password(self, new_pass: str):
		if len(new_pass) < 6:
			raise ValueError("Password must be at least 6 characters long")
		
		hash_object = hashlib.sha256(new_pass.encode())
		self._password_hash = hash_object.hexdigest()

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
	
	def __str__(self) -> str:
		"""Return string representation of the user"""
		return f"User({self._user_id}): {self._name} ({self._role})"
	
	def is_admin(self) -> bool:
		"""Returns true if the user is an admin"""
		return self._role == "admin"
	
	def check_password(self, plain_password: str) -> bool:
		"""Compare plain password to stored SHA-256 hash"""
		return hashlib.sha256(plain_password.encode()).hexdigest() == self._password_hash
	
	