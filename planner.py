"""最小 Planner：根据 state 决定下一课。"""


from lessons import get_lesson, last_lesson_id


def choose_next_lesson(state):
    """优先复习薄弱课；否则返回当前课程。"""
    current_id = state.get("current_lesson", 1)
    return get_lesson(current_id)


def apply_review_result(state, lesson, result):
    """根据 Critic 结果更新进度和下一课。"""
    lesson_id = lesson["id"]


    if result["passed"]:
        completed = state.setdefault("completed_lessons", [])
        if lesson_id not in completed:
            completed.append(lesson_id)


        concepts = state.setdefault("known_concepts", [])
        if lesson["weak_point"] not in concepts:
            concepts.append(lesson["weak_point"])


        if lesson["weak_point"] in state.setdefault("weak_points", []):
            state["weak_points"].remove(lesson["weak_point"])


        if lesson_id < last_lesson_id():
            state["current_lesson"] = lesson_id + 1
    else:
        weak_points = state.setdefault("weak_points", [])
        if result["weak_point"] not in weak_points:
            weak_points.append(result["weak_point"])
        state["current_lesson"] = lesson_id


def is_finished(state):
    """判断课程是否全部通过。"""
    return len(state.get("completed_lessons", [])) >= last_lesson_id()
