from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from pathlib import Path

from database import engine, Base
import models

from routes import users, dashboard, analysis



# Initialize FastAPI
app = FastAPI(
    title="EmailX-Ray API",
    description="Email Threat Detection and Analysis System",
    version="1.0.0"
)


# Frontend directory
BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"


# Create MySQL tables
Base.metadata.create_all(bind=engine)


# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Serve CSS and JavaScript files
if (FRONTEND_DIR / "css").is_dir():
    app.mount(
        "/css",
        StaticFiles(directory=FRONTEND_DIR / "css"),
        name="css"
    )

if (FRONTEND_DIR / "js").is_dir():
    app.mount(
        "/js",
        StaticFiles(directory=FRONTEND_DIR / "js"),
        name="js"
    )


# Function to serve HTML pages
def serve_page(filename):

    file_path = FRONTEND_DIR / filename

    if not file_path.is_file():
        raise HTTPException(
            status_code=404,
            detail=f"{filename} not found"
        )

    return FileResponse(file_path)


# HOME PAGE
@app.get("/", include_in_schema=False)
def home_page():
    return serve_page("index.html")


# LOGIN PAGE
@app.get("/login", include_in_schema=False)
@app.get("/login.html", include_in_schema=False)
def login_page():
    return serve_page("login.html")


# REGISTER PAGE
@app.get("/register", include_in_schema=False)
@app.get("/register.html", include_in_schema=False)
def register_page():
    return serve_page("register.html")


# DASHBOARD PAGE
@app.get("/dashboard", include_in_schema=False)
def dashboard_page():
    return serve_page("dashboard.html")


# EMAIL ANALYSIS PAGE
@app.get("/analyze", include_in_schema=False)
def analyze_page():
    return serve_page("analyze.html")


# HISTORY PAGE
@app.get("/history", include_in_schema=False)
def history_page():
    return serve_page("history.html")


# PROFILE PAGE
@app.get("/profile", include_in_schema=False)
def profile_page():
    return serve_page("profile.html")


# API ROUTES
app.include_router(users.router)
app.include_router(dashboard.router)
app.include_router(analysis.router)


# HEALTH CHECK
@app.get("/health")
def health():
    return {
        "status": "healthy",
        "application": "EmailX-Ray"
    }