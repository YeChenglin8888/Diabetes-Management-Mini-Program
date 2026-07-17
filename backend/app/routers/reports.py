from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.weekly_report import build_weekly_report
from app.utils import success

router = APIRouter(prefix="/reports", tags=["数据周报"])


@router.get("/weekly")
def weekly_report(userId: int, weekStart: str, weekEnd: str, db: Session = Depends(get_db)):
    return success(build_weekly_report(userId, weekStart, weekEnd, db))
