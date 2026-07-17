from decimal import Decimal

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import DietItem, DietRecord, Food
from app.schemas import DietCalculateRequest, DietSaveRequest
from app.utils import day_end, day_start, fail, money2, nutrition_value, parse_date, parse_datetime, success

router = APIRouter(prefix="/diets", tags=["饮食记录"])


def calculate_nutrition(food: Food, weight_g: Decimal) -> dict:
    carb = nutrition_value(food.carb_per_100g, weight_g)
    protein = nutrition_value(food.protein_per_100g or 0, weight_g)
    fat = nutrition_value(food.fat_per_100g or 0, weight_g)
    fiber = nutrition_value(food.fiber_per_100g or 0, weight_g)
    sugar = nutrition_value(food.sugar_per_100g or 0, weight_g)
    starch = nutrition_value(food.starch_per_100g or 0, weight_g)
    calories = money2(carb * Decimal("4") + protein * Decimal("4") + fat * Decimal("9"))
    return {
        "carb": carb,
        "protein": protein,
        "fat": fat,
        "fiber": fiber,
        "sugar": sugar,
        "starch": starch,
        "calories": calories,
    }


def diet_to_dict(diet: DietRecord) -> dict:
    return {
        "dietId": diet.diet_id,
        "userId": diet.user_id,
        "mealType": diet.meal_type,
        "mealTime": diet.meal_time.strftime("%Y-%m-%d %H:%M:%S"),
        "totalCarb": float(diet.total_carb or 0),
        "totalProtein": float(diet.total_protein or 0),
        "totalFat": float(diet.total_fat or 0),
        "totalFiber": float(diet.total_fiber or 0),
        "fastCarbTotal": float(diet.fast_carb_total or 0),
        "slowCarbTotal": float(diet.slow_carb_total or 0),
        "remark": diet.remark,
    }


@router.post("/calculate")
def calculate(payload: DietCalculateRequest, db: Session = Depends(get_db)):
    food = db.get(Food, payload.foodId)
    if not food:
        return fail(404, "食物不存在")
    weight = Decimal(str(payload.weightG))
    values = calculate_nutrition(food, weight)
    return success(
        {
            "foodId": food.food_id,
            "foodName": food.food_name,
            "category": food.category,
            "weightG": float(weight),
            "carbValue": float(values["carb"]),
            "proteinValue": float(values["protein"]),
            "fatValue": float(values["fat"]),
            "fiberValue": float(values["fiber"]),
            "sugarValue": float(values["sugar"]),
            "starchValue": float(values["starch"]),
            "calories": float(values["calories"]),
            "carbType": food.carb_type or "混合碳",
            "giLevel": food.gi_level,
        }
    )


@router.get("")
def list_diets(
    userId: int,
    startDate: str | None = Query(default=None),
    endDate: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    stmt = select(DietRecord).where(DietRecord.user_id == userId)
    if startDate:
        stmt = stmt.where(DietRecord.meal_time >= day_start(parse_date(startDate)))
    if endDate:
        stmt = stmt.where(DietRecord.meal_time <= day_end(parse_date(endDate)))
    records = db.scalars(stmt.order_by(DietRecord.meal_time.desc())).all()
    return success([diet_to_dict(record) for record in records])


@router.post("")
def save_diet(payload: DietSaveRequest, db: Session = Depends(get_db)):
    if not payload.items:
        return fail(400, "饮食明细不能为空")

    diet = DietRecord(
        user_id=payload.userId,
        meal_type=payload.mealType,
        meal_time=parse_datetime(payload.mealTime),
        total_carb=Decimal("0"),
        total_protein=Decimal("0"),
        total_fat=Decimal("0"),
        total_fiber=Decimal("0"),
        fast_carb_total=Decimal("0"),
        slow_carb_total=Decimal("0"),
        remark=payload.remark,
    )
    totals = {
        "carb": Decimal("0"),
        "protein": Decimal("0"),
        "fat": Decimal("0"),
        "fiber": Decimal("0"),
        "fastCarb": Decimal("0"),
        "slowCarb": Decimal("0"),
    }
    for item in payload.items:
        food = db.get(Food, item.foodId)
        if not food:
            return fail(404, f"食物不存在：{item.foodId}")
        weight = Decimal(str(item.weightG))
        values = calculate_nutrition(food, weight)
        carb_type = food.carb_type or "混合碳"
        totals["carb"] += values["carb"]
        totals["protein"] += values["protein"]
        totals["fat"] += values["fat"]
        totals["fiber"] += values["fiber"]
        if carb_type == "快碳":
            totals["fastCarb"] += values["carb"]
        elif carb_type == "慢碳":
            totals["slowCarb"] += values["carb"]
        diet.items.append(
            DietItem(
                food_id=food.food_id,
                weight_g=weight,
                carb_value=values["carb"],
                protein_value=values["protein"],
                fat_value=values["fat"],
                fiber_value=values["fiber"],
                sugar_value=values["sugar"],
                starch_value=values["starch"],
                carb_type=carb_type,
            )
        )

    diet.total_carb = money2(totals["carb"])
    diet.total_protein = money2(totals["protein"])
    diet.total_fat = money2(totals["fat"])
    diet.total_fiber = money2(totals["fiber"])
    diet.fast_carb_total = money2(totals["fastCarb"])
    diet.slow_carb_total = money2(totals["slowCarb"])
    db.add(diet)
    db.commit()
    db.refresh(diet)
    return success(diet_to_dict(diet), "保存成功")
