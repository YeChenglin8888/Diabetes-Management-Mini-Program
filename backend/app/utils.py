from __future__ import annotations

import hashlib
from datetime import date, datetime, time
from decimal import Decimal, ROUND_HALF_UP
from typing import Any


def success(data: Any = None, message: str = "success") -> dict[str, Any]:
    return {"code": 200, "message": message, "data": data if data is not None else {}}


def fail(code: int, message: str, data: Any = None) -> dict[str, Any]:
    return {"code": code, "message": message, "data": data if data is not None else {}}


def password_hash(password: str) -> str:
    return hashlib.sha256(f"diabetes-demo:{password}".encode("utf-8")).hexdigest()


def verify_password(password: str, stored_hash: str) -> bool:
    if stored_hash == "demo_hash_not_for_production" and password == "123456":
        return True
    return password_hash(password) == stored_hash


def parse_datetime(value: str) -> datetime:
    normalized = value.replace("T", " ")
    return datetime.strptime(normalized, "%Y-%m-%d %H:%M:%S")


def parse_date(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d").date()


def day_start(value: date) -> datetime:
    return datetime.combine(value, time.min)


def day_end(value: date) -> datetime:
    return datetime.combine(value, time.max)


def money2(value: Decimal | float | int) -> Decimal:
    return Decimal(str(value)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def glucose_status(measure_type: str, glucose_value: Decimal | float) -> str:
    value = Decimal(str(glucose_value))
    if value < Decimal("3.9"):
        return "偏低"
    if "空腹" in measure_type and value > Decimal("7.0"):
        return "偏高"
    if "后" in measure_type and value > Decimal("10.0"):
        return "偏高"
    return "正常"


def build_weekly_suggestion(high_count: int, low_count: int, avg_daily_carb: Decimal) -> str:
    if low_count > 0:
        return "本周存在低血糖记录，建议关注低血糖风险，必要时及时补充碳水并咨询医生。"
    if high_count >= 2:
        return "本周血糖偏高次数较多，建议减少精制主食、甜食和含糖饮料摄入。"
    if avg_daily_carb > Decimal("180"):
        return "本周日均碳水摄入偏高，建议增加蔬菜和优质蛋白比例，控制主食重量。"
    return "本周血糖整体较稳定，建议继续保持规律饮食和持续记录。"
