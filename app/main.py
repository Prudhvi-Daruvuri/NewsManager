from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import news
from .mongo import MongoClient
from .config import Settings

app = FastAPI(
    title=Settings.PROJECT_NAME,
    description=Settings.PROJECT_DESCRIPTION,
    version=Settings.PROJECT_VERSION
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=Settings.CORS_ORIGINS,
    allow_credentials=Settings.CORS_CREDENTIALS,
    allow_methods=Settings.CORS_METHODS,
    allow_headers=Settings.CORS_HEADERS,
)

@app.on_event("startup")
def startup_db_client():
    MongoClient.connect_to_mongo()

@app.on_event("shutdown")
def shutdown_db_client():
    MongoClient.close_mongo_connection()

# Include routers
app.include_router(news.router)

@app.get("/")
def root():
    return {"message": f"Welcome to {Settings.PROJECT_NAME} API"}
