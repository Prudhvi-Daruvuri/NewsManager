import os
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class MongoConfig:
    MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    NEWS_DATABASE = os.getenv("MONGODB_DB_NAME", "news_manager")
    NEWS_COLLECTION = os.getenv("MONGODB_COLLECTION", "news")

class Settings:
    PROJECT_NAME = "NewsManager"
    PROJECT_VERSION = "1.0.0"
    PROJECT_DESCRIPTION = "A FastAPI-based news management system"
    
    # CORS Configuration
    default_origins = ["http://54.167.37.145:8080", "http://localhost:8080", "http://localhost:8000"]
    CORS_ORIGINS = json.loads(os.getenv("CORS_ORIGINS", json.dumps(default_origins)))
    CORS_CREDENTIALS = True
    CORS_METHODS = ["*"]
    CORS_HEADERS = ["*"]
    
    mongo = MongoConfig
