"""Critic：优先用模型批改，失败时回退到关键词规则。"""

import json
import os
import urllib.request


def keyword_review(lesson, answer):
    """根据课程关键词批改答案，返回结构化检查结果。"""
    normalized = answer.lower()
    matched = [word for word in lesson["keywords"] if word.lower() in normalized]
    passed = len(matched) >= 2

    if passed:
        feedback = "回答通过：已经覆盖关键概念。"
    else:
        feedback = "回答还不够完整：建议补充 " + "、".join(lesson["keywords"][:3])

    return {
        "passed": passed,
        "matched_keywords": matched,
        "feedback": feedback,
        "weak_point": None if passed else lesson["weak_point"],
        "reviewer": "keyword",
    }


def review_answer(lesson, answer, use_llm=None):
    """批改答案；设置 OPENAI_API_KEY 后可使用 OpenAI Responses API。"""
    if use_llm is None:
        use_llm = bool(os.getenv("OPENAI_API_KEY"))
    if not use_llm:
        return keyword_review(lesson, answer)

    try:
        return llm_review(lesson, answer)
    except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        result = keyword_review(lesson, answer)
        result["feedback"] += f"（模型批改失败，已回退关键词规则：{exc}）"
        return result


def llm_review(lesson, answer):
    """调用 OpenAI 批改答案，并规范成 demo 使用的结果结构。"""
    api_key = os.environ["OPENAI_API_KEY"]
    model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
    payload = {
        "model": model,
        "input": build_review_prompt(lesson, answer),
    }
    request = urllib.request.Request(
        "https://api.openai.com/v1/responses",
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    with urllib.request.urlopen(request, timeout=30) as response:
        data = json.loads(response.read().decode("utf-8"))

    parsed = json.loads(strip_code_fence(extract_response_text(data)))
    return normalize_llm_result(lesson, parsed)


def build_review_prompt(lesson, answer):
    """生成批改提示词，要求模型只返回 JSON。"""
    return f"""你是 AI Agent 学习助手的 Critic。请批改用户练习答案。
只返回 JSON，不要输出 Markdown。
JSON 格式：{{"passed": true, "feedback": "...", "matched_keywords": ["..."], "weak_point": null}}

课程标题：{lesson['title']}
课程目标：{lesson['objective']}
练习题：{lesson['exercise']}
参考关键词：{', '.join(lesson['keywords'])}
薄弱点标签：{lesson['weak_point']}
用户答案：{answer}
"""


def extract_response_text(data):
    """从 Responses API 结果中取出文本。"""
    if data.get("output_text"):
        return data["output_text"]

    parts = []
    for item in data.get("output", []):
        for content in item.get("content", []):
            text = content.get("text")
            if text:
                parts.append(text)
    return "".join(parts)


def strip_code_fence(text):
    """兼容模型意外返回的 JSON 代码块。"""
    text = text.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        return "\n".join(lines[1:-1]).strip()
    return text


def normalize_llm_result(lesson, parsed):
    """校验模型批改结果，避免影响主循环字段。"""
    passed = bool(parsed["passed"])
    matched = parsed.get("matched_keywords") or []
    if not isinstance(matched, list):
        matched = []
    return {
        "passed": passed,
        "matched_keywords": [str(item) for item in matched],
        "feedback": str(parsed.get("feedback") or "模型已完成批改。"),
        "weak_point": None if passed else lesson["weak_point"],
        "reviewer": "llm",
    }
