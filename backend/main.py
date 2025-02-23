import os
from dotenv import load_dotenv

load_dotenv()
APPWRITE_ENDPOINT = os.getenv("APPWRITE_ENDPOINT")
APPWRITE_PROJECT_ID = os.getenv("APPWRITE_PROJECT_ID")
APPWRITE_API_KEY = os.getenv("APPWRITE_API_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")
USERS_COLLECTION_ID = os.getenv("USERS_COLLECTION_ID")
WORKOUTS_COLLECTION_ID = os.getenv("WORKOUTS_COLLECTION_ID")
REWARDS_COLLECTION_ID = os.getenv("REWARDS_COLLECTION_ID")