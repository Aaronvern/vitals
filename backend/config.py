import os
from dotenv import load_dotenv

 
load_dotenv()


APPWRITE_ENDPOINT = os.getenv("APPWRITE_ENDPOINT")
APPWRITE_PROJECT_ID = os.getenv("APPWRITE_PROJECT_ID")
APPWRITE_API_KEY = os.getenv("APPWRITE_API_KEY")
APPWRITE_DATABASE_ID = os.getenv("APPWRITE_DATABASE_ID")
SECRET_KEY = os.getenv("SECRET_KEY")
USERS_COLLECTION_ID = os.getenv("USERS_COLLECTION_ID")
WORKOUTS_COLLECTION_ID = os.getenv("WORKOUTS_COLLECTION_ID")
REWARDS_COLLECTION_ID = os.getenv("REWARDS_COLLECTION_ID")


required_vars = [
    "APPWRITE_ENDPOINT", "APPWRITE_PROJECT_ID", "APPWRITE_API_KEY", "APPWRITE_DATABASE_ID",
    "SECRET_KEY", "USERS_COLLECTION_ID", "WORKOUTS_COLLECTION_ID", "REWARDS_COLLECTION_ID"
]
for var in required_vars:
    if not os.getenv(var):
        raise ValueError(f"Missing env : {var}")