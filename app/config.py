import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class MongoConfig:
    MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    DB_NAME = os.getenv("MONGODB_DB_NAME", "news_manager")
    COLLECTION_NAME = os.getenv("MONGODB_COLLECTION", "news")

class Settings:
    PROJECT_NAME = "NewsManager"
    PROJECT_VERSION = "1.0.0"
    PROJECT_DESCRIPTION = "A FastAPI-based news management system"
    
    # CORS Configuration
    CORS_ORIGINS = ["*"]
    CORS_CREDENTIALS = True
    CORS_METHODS = ["*"]
    CORS_HEADERS = ["*"]

    # MongoDB Configuration
    mongo = MongoConfig
