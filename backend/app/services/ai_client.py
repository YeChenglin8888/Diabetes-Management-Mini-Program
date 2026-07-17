from __future__ import annotations

import json

import httpx

from app.config import settings


SYSTEM_PROMPT = (
    "你是糖尿病健康管理助手，只提供饮食、记录和趋势分析建议，"
    "不做诊断、处方或用药调整。遇到持续偏高、低血糖或明显不适，"
    "应提醒用户及时咨询医生或就医。"
)


class AiClientError(Exception):
    pass


def mask_key(value: str) -> str:
    if not value:
        return ""
    if len(value) <= 4:
        return "****"
    return f"****{value[-4:]}"


def call_chat_completion(user_prompt: str) -> str:
    if not settings.ai_api_key:
        raise AiClientError("未配置 AI_API_KEY")

    payload = {
        "model": settings.ai_model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        "stream": False,
        "temperature": 0.4,
    }
    headers = {
        "Authorization": f"Bearer {settings.ai_api_key}",
        "Content-Type": "application/json",
    }

    try:
        with httpx.Client(timeout=settings.ai_timeout_seconds) as client:
            response = client.post(settings.ai_chat_url, json=payload, headers=headers)
            response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        raise AiClientError(f"AI 接口返回异常：{exc.response.status_code}") from exc
    except httpx.RequestError as exc:
        raise AiClientError("AI 接口连接失败") from exc

    try:
        data = json.loads(response.content.decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as exc:
        raise AiClientError("AI 接口返回格式不是 JSON") from exc
    choices = data.get("choices") or []
    if not choices:
        raise AiClientError("AI 接口未返回内容")
    message = choices[0].get("message") or {}
    content = str(message.get("content") or "").strip()
    if not content:
        raise AiClientError("AI 接口返回内容为空")
    return content
