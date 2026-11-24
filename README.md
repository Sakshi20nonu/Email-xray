# EmailXRay

### AI-Assisted Email Threat Analysis Platform

EmailXRay is a web-based email security analysis platform designed to help users identify suspicious emails and understand potential email threats.

The platform allows users to register, authenticate, submit email content for analysis, view threat assessment results and maintain a history of previously analyzed emails.

## Features

- User Registration and Login
- JWT-Based Authentication
- Secure Password Hashing
- Email Threat Analysis
- Risk Score and Threat Classification
- Detection of Suspicious Email Indicators
- Personalized Dashboard
- Analysis History
- User Profile Management
- MySQL Database Integration

## Technologies Used

**Frontend**
- HTML5
- CSS3
- JavaScript

**Backend**
- Python
- FastAPI
- SQLAlchemy

**Database**
- MySQL

**Authentication**
- JSON Web Tokens (JWT)
- Bcrypt Password Hashing

## Project Structure

- `backend/` – Backend application and API routes.
- `frontend/` – User interface and frontend pages.
- `.env.example` – Environment configuration template.
- `requirements.txt` – Python dependencies.

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_REPOSITORY_URL
```

### 2. Navigate to the project directory

```bash
cd EmailXRay
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the environment

Windows:

```bash
venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure environment variables

Create a `.env` file using `.env.example` as a reference.

Update the MySQL connection details and JWT secret key.

### 7. Create the MySQL database

```sql
CREATE DATABASE emailxray;
```

### 8. Start the FastAPI server

Navigate to the backend directory:

```bash
cd backend
```

Run:

```bash
python -m uvicorn main:app --reload
```

### 9. Open the application

Visit:

http://127.0.0.1:8000

API documentation:

http://127.0.0.1:8000/docs

## Project Status

EmailXRay is an academic cybersecurity mini-project focused on email threat analysis, user authentication and security-oriented web application development.