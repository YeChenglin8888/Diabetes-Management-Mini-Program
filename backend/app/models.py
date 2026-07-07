from sqlalchemy import Date, DateTime, ForeignKey, Integer, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class User(Base):
    __tablename__ = "user"

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[str | None] = mapped_column(String(20), unique=True)
    gender: Mapped[str | None] = mapped_column(String(10))
    age: Mapped[int | None] = mapped_column(Integer)
    diabetes_type: Mapped[str | None] = mapped_column(String(30))
    created_at: Mapped[object] = mapped_column(DateTime, server_default=func.now())

    glucose_records: Mapped[list["GlucoseRecord"]] = relationship(back_populates="user")
    diet_records: Mapped[list["DietRecord"]] = relationship(back_populates="user")


class GlucoseRecord(Base):
    __tablename__ = "glucose_record"

    record_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.user_id"), nullable=False)
    measure_time: Mapped[object] = mapped_column(DateTime, nullable=False)
    measure_type: Mapped[str] = mapped_column(String(30), nullable=False)
    glucose_value: Mapped[object] = mapped_column(Numeric(4, 1), nullable=False)
    remark: Mapped[str | None] = mapped_column(String(255))
    created_at: Mapped[object] = mapped_column(DateTime, server_default=func.now())

    user: Mapped[User] = relationship(back_populates="glucose_records")


class Food(Base):
    __tablename__ = "food"

    food_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    food_name: Mapped[str] = mapped_column(String(100), nullable=False)
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    carb_per_100g: Mapped[object] = mapped_column(Numeric(5, 2), nullable=False)
    gi_level: Mapped[str] = mapped_column(String(20), nullable=False)
    created_at: Mapped[object] = mapped_column(DateTime, server_default=func.now())


class DietRecord(Base):
    __tablename__ = "diet_record"

    diet_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.user_id"), nullable=False)
    meal_type: Mapped[str] = mapped_column(String(20), nullable=False)
    meal_time: Mapped[object] = mapped_column(DateTime, nullable=False)
    total_carb: Mapped[object] = mapped_column(Numeric(6, 2), nullable=False, default=0)
    remark: Mapped[str | None] = mapped_column(String(255))
    created_at: Mapped[object] = mapped_column(DateTime, server_default=func.now())

    user: Mapped[User] = relationship(back_populates="diet_records")
    items: Mapped[list["DietItem"]] = relationship(cascade="all, delete-orphan")


class DietItem(Base):
    __tablename__ = "diet_item"

    item_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    diet_id: Mapped[int] = mapped_column(ForeignKey("diet_record.diet_id"), nullable=False)
    food_id: Mapped[int] = mapped_column(ForeignKey("food.food_id"), nullable=False)
    weight_g: Mapped[object] = mapped_column(Numeric(6, 2), nullable=False)
    carb_value: Mapped[object] = mapped_column(Numeric(6, 2), nullable=False)

    food: Mapped[Food] = relationship()


class Recipe(Base):
    __tablename__ = "recipe"

    recipe_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    recipe_name: Mapped[str] = mapped_column(String(100), nullable=False)
    meal_type: Mapped[str] = mapped_column(String(20), nullable=False)
    ingredients: Mapped[str] = mapped_column(Text, nullable=False)
    steps: Mapped[str] = mapped_column(Text, nullable=False)
    recommend_reason: Mapped[str] = mapped_column(Text, nullable=False)
    suitable_people: Mapped[str | None] = mapped_column(String(255))
    created_at: Mapped[object] = mapped_column(DateTime, server_default=func.now())


class WeeklyReport(Base):
    __tablename__ = "weekly_report"

    report_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.user_id"), nullable=False)
    week_start: Mapped[object] = mapped_column(Date, nullable=False)
    week_end: Mapped[object] = mapped_column(Date, nullable=False)
    avg_glucose: Mapped[object | None] = mapped_column(Numeric(4, 1))
    max_glucose: Mapped[object | None] = mapped_column(Numeric(4, 1))
    min_glucose: Mapped[object | None] = mapped_column(Numeric(4, 1))
    high_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    low_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    total_carb: Mapped[object] = mapped_column(Numeric(7, 2), nullable=False, default=0)
    avg_daily_carb: Mapped[object] = mapped_column(Numeric(6, 2), nullable=False, default=0)
    suggestion: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[object] = mapped_column(DateTime, server_default=func.now())
