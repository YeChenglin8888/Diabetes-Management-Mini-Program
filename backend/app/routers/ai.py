import json
from datetime import date, timedelta

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models import User
from app.schemas import AiChatRequest, WeeklyAnalysisRequest
from app.services.ai_client import AiClientError, call_chat_completion, mask_key
from app.services.weekly_report import build_weekly_report
from app.utils import fail, success

router = APIRouter(prefix="/ai", tags=["AI分析"])


@router.get("/config")
def ai_config():
    return success(
        {
            "configured": bool(settings.ai_api_key),
            "apiBase": settings.ai_api_base,
            "chatPath": settings.ai_chat_path,
            "model": settings.ai_model,
            "keyMasked": mask_key(settings.ai_api_key),
        }
    )


@router.post("/reports/weekly-analysis")
def weekly_analysis(payload: WeeklyAnalysisRequest, db: Session = Depends(get_db)):
    user = db.get(User, payload.userId)
    if not user:
        return fail(404, "用户不存在")

    report = build_weekly_report(payload.userId, payload.weekStart, payload.weekEnd, db)
    prompt = build_weekly_analysis_prompt(user, report)
    try:
        analysis = call_chat_completion(prompt)
        return success({"analysis": analysis, "fallback": False})
    except AiClientError as exc:
        return success(
            {
                "analysis": report.get("suggestion") or "继续保持规律记录，并结合血糖和饮食趋势复盘。",
                "fallback": True,
                "error": str(exc),
            }
        )


@router.post("/chat")
def chat(payload: AiChatRequest, db: Session = Depends(get_db)):
    user = db.get(User, payload.userId)
    if not user:
        return fail(404, "用户不存在")

    week_end = payload.weekEnd or date.today().strftime("%Y-%m-%d")
    week_start = payload.weekStart or (date.today() - timedelta(days=6)).strftime("%Y-%m-%d")
    report = build_weekly_report(payload.userId, week_start, week_end, db)
    prompt = build_chat_prompt(user, report, payload)
    try:
        answer = call_chat_completion(prompt)
        return success({"answer": answer, "fallback": False})
    except AiClientError as exc:
        return success(
            {
                "answer": "AI 服务暂时不可用。可以先查看周报建议；如血糖持续偏高、偏低或身体不适，请及时咨询医生。",
                "fallback": True,
                "error": str(exc),
            }
        )


def build_weekly_analysis_prompt(user: User, report: dict) -> str:
    profile = {
        "gender": user.gender,
        "age": user.age,
        "diabetesType": user.diabetes_type,
    }
    report_data = {
        "weekStart": report.get("weekStart"),
        "weekEnd": report.get("weekEnd"),
        "avgGlucose": report.get("avgGlucose"),
        "maxGlucose": report.get("maxGlucose"),
        "minGlucose": report.get("minGlucose"),
        "highCount": report.get("highCount"),
        "lowCount": report.get("lowCount"),
        "totalCarb": report.get("totalCarb"),
        "avgDailyCarb": report.get("avgDailyCarb"),
        "totalProtein": report.get("totalProtein"),
        "totalFat": report.get("totalFat"),
        "totalFiber": report.get("totalFiber"),
        "fastCarbTotal": report.get("fastCarbTotal"),
        "slowCarbTotal": report.get("slowCarbTotal"),
        "fastCarbRatio": report.get("fastCarbRatio"),
        "ruleSuggestion": report.get("suggestion"),
    }
    return (
        "请基于以下脱敏健康管理数据，生成一段适合小程序展示的中文周报解读。\n"
        "要求：1. 分为“本周概况、需要关注、下周建议”三段；"
        "2. 语气温和、简洁；3. 不输出诊断、处方或用药调整；"
        "4. 如有低血糖或多次偏高，提醒咨询医生。\n"
        f"用户基础信息：{json.dumps(profile, ensure_ascii=False)}\n"
        f"周报统计数据：{json.dumps(report_data, ensure_ascii=False)}"
    )


def build_chat_prompt(user: User, report: dict, payload: AiChatRequest) -> str:
    profile = {
        "gender": user.gender,
        "age": user.age,
        "diabetesType": user.diabetes_type,
    }
    report_data = {
        "weekStart": report.get("weekStart"),
        "weekEnd": report.get("weekEnd"),
        "avgGlucose": report.get("avgGlucose"),
        "maxGlucose": report.get("maxGlucose"),
        "minGlucose": report.get("minGlucose"),
        "highCount": report.get("highCount"),
        "lowCount": report.get("lowCount"),
        "totalCarb": report.get("totalCarb"),
        "avgDailyCarb": report.get("avgDailyCarb"),
        "fastCarbRatio": report.get("fastCarbRatio"),
        "ruleSuggestion": report.get("suggestion"),
    }
    history = [
        {"role": item.role, "content": item.content}
        for item in payload.history[-6:]
        if item.role in {"user", "assistant"} and item.content
    ]
    return (
        "请作为糖尿病健康管理问答助手，结合脱敏用户资料和近 7 天统计数据回答用户问题。\n"
        "边界：不诊断疾病，不开处方，不建议自行调整用药；涉及持续异常、低血糖、明显不适时提醒就医。\n"
        "回答要求：中文、具体、可执行，优先结合血糖和饮食记录，不超过 300 字。\n"
        f"用户基础信息：{json.dumps(profile, ensure_ascii=False)}\n"
        f"近 7 天统计：{json.dumps(report_data, ensure_ascii=False)}\n"
        f"最近对话：{json.dumps(history, ensure_ascii=False)}\n"
        f"用户当前问题：{payload.question}"
    )
