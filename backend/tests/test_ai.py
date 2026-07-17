from app.models import User
from app.routers.ai import build_chat_prompt, build_weekly_analysis_prompt
from app.schemas import AiChatRequest
from app.services.ai_client import mask_key


def test_mask_key():
    assert mask_key("") == ""
    assert mask_key("abc") == "****"
    assert mask_key("sk-test-1234") == "****1234"


def test_weekly_analysis_prompt_is_desensitized():
    user = User(
        username="private_name",
        phone="13800000000",
        gender="男",
        age=45,
        diabetes_type="2型糖尿病",
    )
    report = {
        "weekStart": "2026-07-02",
        "weekEnd": "2026-07-08",
        "avgGlucose": 6.8,
        "highCount": 1,
        "lowCount": 0,
        "totalCarb": 560,
        "suggestion": "继续保持规律记录。",
    }

    prompt = build_weekly_analysis_prompt(user, report)

    assert "private_name" not in prompt
    assert "13800000000" not in prompt
    assert "2型糖尿病" in prompt
    assert "avgGlucose" in prompt


def test_chat_prompt_is_desensitized_and_keeps_question():
    user = User(
        username="private_name",
        phone="13800000000",
        gender="女",
        age=52,
        diabetes_type="2型糖尿病",
    )
    report = {
        "weekStart": "2026-07-02",
        "weekEnd": "2026-07-08",
        "avgGlucose": 7.1,
        "highCount": 2,
        "suggestion": "本周血糖偏高次数较多。",
    }
    payload = AiChatRequest(userId=1, question="我晚餐主食怎么吃？")

    prompt = build_chat_prompt(user, report, payload)

    assert "private_name" not in prompt
    assert "13800000000" not in prompt
    assert "我晚餐主食怎么吃？" in prompt
    assert "avgGlucose" in prompt
