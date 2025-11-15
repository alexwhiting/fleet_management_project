from models.user import User
from models.truck import Truck
from models.battery import Battery
from models.telemetry import TelemetryRecord
from services.analytics_engine import AnalyticsEngine
from database_manager import load_all, save_users


users = []
trucks = []
batteries = []
