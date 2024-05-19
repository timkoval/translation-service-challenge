from dotenv import load_dotenv
import os

load_dotenv()

MONGO_DB = os.environ.get("MONGO_DB")
MONGO_URL = os.environ.get("MONGO_URL")
MONGO_USER = os.environ.get("MONGO_USER")
MONGO_PASSWORD = os.environ.get("MONGO_PASSWORD")
MAX_CONNECTIONS_COUNT = os.environ.get("MAX_CONNECTIONS_COUNT")
MIN_CONNECTIONS_COUNT = os.environ.get("MIN_CONNECTIONS_COUNT")

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
