from decimal import Decimal

from app.utils import build_weekly_suggestion, glucose_status, money2


def test_glucose_status_rules():
    assert glucose_status("空腹", Decimal("7.2")) == "偏高"
    assert glucose_status("早餐后", Decimal("10.5")) == "偏高"
    assert glucose_status("睡前", Decimal("3.8")) == "偏低"
    assert glucose_status("空腹", Decimal("6.8")) == "正常"


def test_carb_rounding_formula():
    assert money2(Decimal("40") / Decimal("100") * Decimal("66.90")) == Decimal("26.76")


def test_weekly_suggestion_priority():
    assert "低血糖" in build_weekly_suggestion(3, 1, Decimal("120"))
    assert "偏高" in build_weekly_suggestion(2, 0, Decimal("120"))
