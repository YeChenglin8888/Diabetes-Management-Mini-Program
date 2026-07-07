from fastapi import APIRouter, Depends
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.schemas import LoginRequest, RegisterRequest
from app.utils import fail, password_hash, success, verify_password

router = APIRouter(prefix="/auth", tags=["用户管理"])


@router.post("/register")
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    conditions = [User.username == payload.username]
    if payload.phone:
        conditions.append(User.phone == payload.phone)
    exists = db.scalar(select(User).where(or_(*conditions)))
    if exists:
        return fail(400, "用户名或手机号已存在")

    user = User(
        username=payload.username,
        password_hash=password_hash(payload.password),
        phone=payload.phone,
        gender=payload.gender,
        age=payload.age,
        diabetes_type=payload.diabetesType,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return success({"userId": user.user_id, "username": user.username}, "注册成功")


@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.scalar(
        select(User).where(or_(User.username == payload.username, User.phone == payload.username))
    )
    if not user or not verify_password(payload.password, user.password_hash):
        return fail(401, "账号或密码错误")

    return success(
        {
            "userId": user.user_id,
            "username": user.username,
            "phone": user.phone,
            "gender": user.gender,
            "age": user.age,
            "diabetesType": user.diabetes_type,
        },
        "登录成功",
    )
