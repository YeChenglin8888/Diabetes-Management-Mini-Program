from decimal import Decimal

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import DietRecord, GlucoseRecord, WeeklyReport
from app.utils import (
    build_weekly_suggestion,
    day_end,
    day_start,
    glucose_status,
    money2,
    parse_date,
    success,
)

router = APIRouter(prefix="/reports", tags=["数据周报"])


@router.get("/weekly")
def weekly_report(userId: int, weekStart: str, weekEnd: str, db: Session = Depends(get_db)):
    start = parse_date(weekStart)
    end = parse_date(weekEnd)
    glucose_records = db.scalars(
        select(GlucoseRecord).where(
            GlucoseRecord.user_id == userId,
            GlucoseRecord.measure_time >= day_start(start),
            GlucoseRecord.measure_time <= day_end(end),
        )
    ).all()
    diet_records = db.scalars(
        select(DietRecord).where(
            DietRecord.user_id == userId,
            DietRecord.meal_time >= day_start(start),
            DietRecord.meal_time <= day_end(end),
        )
    ).all()

    glucose_values = [Decimal(record.glucose_value) for record in glucose_records]
    avg_glucose = money2(sum(glucose_values) / len(glucose_values)) if glucose_values else None
    max_glucose = max(glucose_values) if glucose_values else None
    min_glucose = min(glucose_values) if glucose_values else None
    high_count = sum(
        1 for record in glucose_records if glucose_status(record.measure_type, record.glucose_value) == "偏高"
    )
    low_count = sum(
        1 for record in glucose_records if glucose_status(record.measure_type, record.glucose_value) == "偏低"
    )
    total_carb = money2(sum((Decimal(record.total_carb) for record in diet_records), Decimal("0")))
    days = max((end - start).days + 1, 1)
    avg_daily_carb = money2(total_carb / Decimal(days))
    suggestion = build_weekly_suggestion(high_count, low_count, avg_daily_carb)

    report = db.scalar(
        select(WeeklyReport).where(
            WeeklyReport.user_id == userId,
            WeeklyReport.week_start == start,
            WeeklyReport.week_end == end,
        )
    )
    if not report:
        report = WeeklyReport(user_id=userId, week_start=start, week_end=end)
        db.add(report)
    report.avg_glucose = avg_glucose
    report.max_glucose = max_glucose
    report.min_glucose = min_glucose
    report.high_count = high_count
    report.low_count = low_count
    report.total_carb = total_carb
    report.avg_daily_carb = avg_daily_carb
    report.suggestion = suggestion
    db.commit()

    return success(
        {
            "weekStart": weekStart,
            "weekEnd": weekEnd,
            "avgGlucose": float(avg_glucose) if avg_glucose is not None else None,
            "maxGlucose": float(max_glucose) if max_glucose is not None else None,
            "minGlucose": float(min_glucose) if min_glucose is not None else None,
            "highCount": high_count,
            "lowCount": low_count,
            "totalCarb": float(total_carb),
            "avgDailyCarb": float(avg_daily_carb),
            "suggestion": suggestion,
        }
    )
