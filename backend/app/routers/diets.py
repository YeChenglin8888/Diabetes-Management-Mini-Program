from decimal import Decimal

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import DietItem, DietRecord, Food
from app.schemas import DietCalculateRequest, DietSaveRequest
from app.utils import fail, money2, parse_datetime, success

router = APIRouter(prefix="/diets", tags=["饮食记录"])


def calculate_carb(food: Food, weight_g: Decimal) -> Decimal:
    return money2(weight_g / Decimal("100") * Decimal(food.carb_per_100g))


@router.post("/calculate")
def calculate(payload: DietCalculateRequest, db: Session = Depends(get_db)):
    food = db.get(Food, payload.foodId)
    if not food:
        return fail(404, "食物不存在")
    weight = Decimal(str(payload.weightG))
    return success(
        {
            "foodId": food.food_id,
            "foodName": food.food_name,
            "weightG": float(weight),
            "carbValue": float(calculate_carb(food, weight)),
        }
    )


@router.post("")
def save_diet(payload: DietSaveRequest, db: Session = Depends(get_db)):
    if not payload.items:
        return fail(400, "饮食明细不能为空")

    diet = DietRecord(
        user_id=payload.userId,
        meal_type=payload.mealType,
        meal_time=parse_datetime(payload.mealTime),
        total_carb=Decimal("0"),
        remark=payload.remark,
    )
    total = Decimal("0")
    for item in payload.items:
        food = db.get(Food, item.foodId)
        if not food:
            return fail(404, f"食物不存在：{item.foodId}")
        weight = Decimal(str(item.weightG))
        carb = calculate_carb(food, weight)
        total += carb
        diet.items.append(DietItem(food_id=food.food_id, weight_g=weight, carb_value=carb))

    diet.total_carb = money2(total)
    db.add(diet)
    db.commit()
    db.refresh(diet)
    return success({"dietId": diet.diet_id, "totalCarb": float(diet.total_carb)}, "保存成功")
