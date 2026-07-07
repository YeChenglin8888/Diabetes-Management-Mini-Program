from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Recipe
from app.utils import fail, success

router = APIRouter(prefix="/recipes", tags=["降糖食谱"])


def recipe_summary(recipe: Recipe) -> dict:
    return {
        "recipeId": recipe.recipe_id,
        "recipeName": recipe.recipe_name,
        "mealType": recipe.meal_type,
        "recommendReason": recipe.recommend_reason,
    }


def recipe_detail(recipe: Recipe) -> dict:
    data = recipe_summary(recipe)
    data.update(
        {
            "ingredients": recipe.ingredients,
            "steps": recipe.steps,
            "suitablePeople": recipe.suitable_people,
        }
    )
    return data


@router.get("")
def list_recipes(mealType: str | None = Query(default=None), db: Session = Depends(get_db)):
    stmt = select(Recipe)
    if mealType:
        stmt = stmt.where(Recipe.meal_type == mealType)
    recipes = db.scalars(stmt.order_by(Recipe.recipe_id)).all()
    return success([recipe_summary(recipe) for recipe in recipes])


@router.get("/{recipeId}")
def get_recipe(recipeId: int, db: Session = Depends(get_db)):
    recipe = db.get(Recipe, recipeId)
    if not recipe:
        return fail(404, "食谱不存在")
    return success(recipe_detail(recipe))
