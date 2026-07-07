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
        "giLevel": food.gi_level,
    }


@router.get("")
def list_foods(
    keyword: str | None = Query(default=None),
    category: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    stmt = select(Food)
    if keyword:
        stmt = stmt.where(Food.food_name.like(f"%{keyword}%"))
    if category:
        stmt = stmt.where(Food.category == category)
    foods = db.scalars(stmt.order_by(Food.category, Food.food_id)).all()
    return success([food_to_dict(food) for food in foods])
