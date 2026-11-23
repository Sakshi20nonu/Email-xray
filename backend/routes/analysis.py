
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import EmailAnalysis, User
from schemas import EmailInput
from auth import get_current_user
from services.email_analyzer import analyze_email

router = APIRouter(prefix="/api/analysis", tags=["Email Analysis"])


@router.post("/analyze")
def analyze(
    data: EmailInput,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    result = analyze_email(
        data.subject,
        data.email_content
    )

    new_analysis = EmailAnalysis(
        user_id=current_user.id,
        subject=data.subject,
        email_content=data.email_content,
        risk_score=result["risk_score"],
        classification=result["classification"],
        indicators=result["indicators"]
    )

    db.add(new_analysis)
    db.commit()
    db.refresh(new_analysis)

    return {
        "message": "Email analysis completed",
        "analysis_id": new_analysis.id,
        "result": result
    }


@router.get("/history")
def analysis_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    records = db.query(EmailAnalysis).filter(
        EmailAnalysis.user_id == current_user.id
    ).order_by(
        EmailAnalysis.id.desc()
    ).all()

    return [
        {
            "id": record.id,
            "subject": record.subject,
            "risk_score": record.risk_score,
            "classification": record.classification,
            "indicators": record.indicators,
            "created_at": record.created_at
        }
        for record in records
    ]


@router.get("/{analysis_id}")
def get_analysis(
    analysis_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    record = db.query(EmailAnalysis).filter(
        EmailAnalysis.id == analysis_id,
        EmailAnalysis.user_id == current_user.id
    ).first()

    if not record:
        raise HTTPException(
            status_code=404,
            detail="Analysis not found"
        )

    return {
        "id": record.id,
        "subject": record.subject,
        "email_content": record.email_content,
        "risk_score": record.risk_score,
        "classification": record.classification,
        "indicators": record.indicators,
        "created_at": record.created_at
    }
