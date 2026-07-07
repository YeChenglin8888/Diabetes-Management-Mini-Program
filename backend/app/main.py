from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import auth, diets, foods, glucose, recipes, reports
from app.utils import success

app = FastAPI(title="糖尿病饮食血糖管理小程序接口", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health", tags=["运行状态"])
def health():
    return success({"status": "ok"})


app.include_router(auth.router, prefix="/api")
app.include_router(glucose.router, prefix="/api")
app.include_router(foods.router, prefix="/api")
app.include_router(diets.router, prefix="/api")
app.include_router(recipes.router, prefix="/api")
app.include_router(reports.router, prefix="/api")
