
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine, Base

import models

from routes import users, dashboard, analysis

app = FastAPI(
    title="EmailX-Ray API",
    description="Email Threat Detection and Analysis System",
    version="1.0.0"
)

# Create MySQL tables
Base.metadata.create_all(bind=engine)

# Allow frontend connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict this to your frontend origin in production
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routes
app.include_router(users.router)
app.include_router(dashboard.router)
app.include_router(analysis.router)


@app.get("/")
def home():
    return {
        "message": "Welcome to EmailX-Ray Backend",
        "status": "Running successfully"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}
