"""最小评测集：验证学习助手 demo 的关键行为。"""

import json
import tempfile
from pathlib import Path

import tools
from main import run_once


def fresh_state():
    """创建一份不依赖 state.json 的干净评测状态。"""
    return {
        "current_lesson": 1,
        "completed_lessons": [],
        "known_concepts": [],
        "weak_points": [],
        "history": [],
        "max_steps": 12,
    }


def test_pass_advances_lesson():
    """回答覆盖关键概念时，应通过并推进到下一课。"""
    state = fresh_state()
    result = run_once(
        state,
        "Agent 会围绕目标使用工具，根据状态和观察结果调整下一步。",
        use_llm=False,
    )
    assert result["passed"] is True
    assert state["current_lesson"] == 2
    assert state["completed_lessons"] == [1]
    assert state["weak_points"] == []


def test_fail_records_weak_point():
    """回答太空时，应停留当前课并记录薄弱点。"""
    state = fresh_state()
    result = run_once(state, "不知道", use_llm=False)
    assert result["passed"] is False
    assert state["current_lesson"] == 1
    assert state["completed_lessons"] == []
    assert state["weak_points"] == ["agent_definition"]


def test_trace_is_jsonl(trace_path):
    """每轮执行都应写入一行可解析的 JSON trace。"""
    if trace_path.exists():
        trace_path.unlink()
    state = fresh_state()
    run_once(state, "目标 工具 状态 下一步", use_llm=False)

    lines = trace_path.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1
    event = json.loads(lines[0])
    assert event["lesson_id"] == 1
    assert event["critic_result"]["passed"] is True
    assert event["before_state"]["current_lesson"] == 1
    assert event["after_state"]["current_lesson"] == 2


def main():
    """运行全部评测用例。"""
    with tempfile.TemporaryDirectory() as tmp_dir:
        tools.TRACE_PATH = Path(tmp_dir) / "trace.jsonl"
        test_pass_advances_lesson()
        test_fail_records_weak_point()
        test_trace_is_jsonl(tools.TRACE_PATH)
    print("eval passed")


if __name__ == "__main__":
    main()
