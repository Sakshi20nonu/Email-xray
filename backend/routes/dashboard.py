
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from sqlalchemy import func

from database import get_db
from models import User, EmailAnalysis
from auth import get_current_user

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])


@router.get("/stats")
def dashboard_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    total = db.query(EmailAnalysis).filter(
        EmailAnalysis.user_id == current_user.id
    ).count()

    safe = db.query(EmailAnalysis).filter(
        EmailAnalysis.user_id == current_user.id,
        EmailAnalysis.classification == "Safe"
    ).count()

    suspicious = db.query(EmailAnalysis).filter(
        EmailAnalysis.user_id == current_user.id,
        EmailAnalysis.classification == "Suspicious"
    ).count()

    high_risk = db.query(EmailAnalysis).filter(
        EmailAnalysis.user_id == current_user.id,
        EmailAnalysis.classification == "High Risk"
    ).count()

    recent = db.query(EmailAnalysis).filter(
        EmailAnalysis.user_id == current_user.id
    ).order_by(
        EmailAnalysis.id.desc()
    ).limit(5).all()

    return {
        "username": current_user.name,
        "total_emails": total,
        "safe_emails": safe,
        "suspicious_emails": suspicious,
        "high_risk_emails": high_risk,
        "recent_analyses": [
            {
                "id": item.id,
                "subject": item.subject,
                "risk_score": item.risk_score,
                "classification": item.classification,
                "created_at": item.created_at
            }
            for item in recent
        ]
    }
