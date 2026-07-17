from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import DietRecord, GlucoseRecord, WeeklyReport
from app.utils import build_weekly_suggestion, day_end, day_start, glucose_status, money2, parse_date


def build_weekly_report(user_id: int, week_start: str, week_end: str, db: Session) -> dict:
    start = parse_date(week_start)
    end = parse_date(week_end)
    glucose_records = db.scalars(
        select(GlucoseRecord).where(
            GlucoseRecord.user_id == user_id,
            GlucoseRecord.measure_time >= day_start(start),
            GlucoseRecord.measure_time <= day_end(end),
        )
    ).all()
    diet_records = db.scalars(
        select(DietRecord).where(
            DietRecord.user_id == user_id,
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
    total_carb = money2(sum((Decimal(record.total_carb or 0) for record in diet_records), Decimal("0")))
    total_protein = money2(sum((Decimal(record.total_protein or 0) for record in diet_records), Decimal("0")))
    total_fat = money2(sum((Decimal(record.total_fat or 0) for record in diet_records), Decimal("0")))
    total_fiber = money2(sum((Decimal(record.total_fiber or 0) for record in diet_records), Decimal("0")))
    fast_carb_total = money2(sum((Decimal(record.fast_carb_total or 0) for record in diet_records), Decimal("0")))
    slow_carb_total = money2(sum((Decimal(record.slow_carb_total or 0) for record in diet_records), Decimal("0")))
    days = max((end - start).days + 1, 1)
    avg_daily_carb = money2(total_carb / Decimal(days))
    fast_carb_ratio = money2(fast_carb_total / total_carb * Decimal("100")) if total_carb > 0 else Decimal("0")
    suggestion = build_weekly_suggestion(high_count, low_count, avg_daily_carb, fast_carb_total)

    report = db.scalar(
        select(WeeklyReport).where(
            WeeklyReport.user_id == user_id,
            WeeklyReport.week_start == start,
            WeeklyReport.week_end == end,
        )
    )
    if not report:
        report = WeeklyReport(user_id=user_id, week_start=start, week_end=end)
        db.add(report)
    report.avg_glucose = avg_glucose
    report.max_glucose = max_glucose
    report.min_glucose = min_glucose
    report.high_count = high_count
    report.low_count = low_count
    report.total_carb = total_carb
    report.avg_daily_carb = avg_daily_carb
    report.total_protein = total_protein
    report.total_fat = total_fat
    report.total_fiber = total_fiber
    report.fast_carb_total = fast_carb_total
    report.slow_carb_total = slow_carb_total
    report.suggestion = suggestion
    db.commit()

    return {
        "weekStart": week_start,
        "weekEnd": week_end,
        "avgGlucose": float(avg_glucose) if avg_glucose is not None else None,
        "maxGlucose": float(max_glucose) if max_glucose is not None else None,
        "minGlucose": float(min_glucose) if min_glucose is not None else None,
        "highCount": high_count,
        "lowCount": low_count,
        "totalCarb": float(total_carb),
        "avgDailyCarb": float(avg_daily_carb),
        "totalProtein": float(total_protein),
        "totalFat": float(total_fat),
        "totalFiber": float(total_fiber),
        "fastCarbTotal": float(fast_carb_total),
        "slowCarbTotal": float(slow_carb_total),
        "fastCarbRatio": float(fast_carb_ratio),
        "suggestion": suggestion,
    }
