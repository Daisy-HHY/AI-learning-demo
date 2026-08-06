"""学习助手 demo 的文件工具。"""


import json

from pathlib import Path

from lessons import first_lesson_id


STATE_PATH = Path(__file__).with_name("state.json")
TRACE_PATH = Path(__file__).with_name("trace.jsonl")


DEFAULT_STATE = {
    "user": "Daisy",
    "current_lesson": first_lesson_id(),
    "completed_lessons": [],
    "known_concepts": [],
    "weak_points": [],
    "history": [],
    "max_steps": 12,
}


def load_state():
    """读取学习状态；文件缺失或格式错误时返回默认状态。"""
    if not STATE_PATH.exists():
        return DEFAULT_STATE.copy()
    try:
        state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return DEFAULT_STATE.copy()


    merged = DEFAULT_STATE.copy()
    merged.update(state)
    return merged


def save_state(state):
    """把学习状态保存到 state.json。"""
    STATE_PATH.write_text(
        json.dumps(state, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def add_history(state, lesson_id, passed, feedback):
    """追加一次答题记录。"""
    state.setdefault("history", []).append({
        "lesson_id": lesson_id,
        "passed": passed,
        "feedback": feedback,
    })


def snapshot_state(state):
    """提取 trace 需要的最小状态快照。"""
    return {
        "current_lesson": state.get("current_lesson"),
        "completed_lessons": list(state.get("completed_lessons", [])),
        "weak_points": list(state.get("weak_points", [])),
        "history_count": len(state.get("history", [])),
    }


def write_trace(event):
    """追加一行 JSONL trace，便于观察 Agent 执行过程。"""
    with TRACE_PATH.open("a", encoding="utf-8") as file:
        file.write(json.dumps(event, ensure_ascii=False) + "\n")
