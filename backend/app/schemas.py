from pydantic import BaseModel, Field


class RegisterRequest(BaseModel):
    username: str
    password: str
    phone: str | None = None
    gender: str | None = None
    age: int | None = None
    diabetesType: str | None = None


class LoginRequest(BaseModel):
    username: str
    password: str


class GlucoseRequest(BaseModel):
    userId: int
    measureTime: str
    measureType: str
    glucoseValue: float = Field(gt=0)
    remark: str | None = None


class GlucoseUpdateRequest(BaseModel):
    measureTime: str | None = None
    measureType: str | None = None
    glucoseValue: float | None = Field(default=None, gt=0)
    remark: str | None = None


class DietCalculateRequest(BaseModel):
    foodId: int
    weightG: float = Field(gt=0)


class DietItemRequest(BaseModel):
    foodId: int
    weightG: float = Field(gt=0)


class DietSaveRequest(BaseModel):
    userId: int
    mealType: str
    mealTime: str
    items: list[DietItemRequest]
    remark: str | None = None
