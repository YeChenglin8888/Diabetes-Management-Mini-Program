from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Food
from app.utils import success

router = APIRouter(prefix="/foods", tags=["食物库"])


def food_to_dict(food: Food) -> dict:
    return {
        "foodId": food.food_id,
        "foodName": food.food_name,
        "category": food.category,
        "carbPer100g": float(food.carb_per_100g),
        "proteinPer100g": float(food.protein_per_100g or 0),
        "fatPer100g": float(food.fat_per_100g or 0),
        "fiberPer100g": float(food.fiber_per_100g or 0),
        "sugarPer100g": float(food.sugar_per_100g or 0),
        "starchPer100g": float(food.starch_per_100g or 0),
        "carbType": food.carb_type or "混合碳",
        "giLevel": food.gi_level,
    }


@router.get("")
def list_foods(
    keyword: str | None = Query(default=None),
    category: str | None = Query(default=None),
    carbType: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    stmt = select(Food)
    if keyword:
        stmt = stmt.where(Food.food_name.like(f"%{keyword}%"))
    if category:
        stmt = stmt.where(Food.category == category)
    if carbType:
        stmt = stmt.where(Food.carb_type == carbType)
    foods = db.scalars(stmt.order_by(Food.category, Food.food_id)).all()
    return success([food_to_dict(food) for food in foods])
