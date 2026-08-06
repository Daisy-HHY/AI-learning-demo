"""AI Agent 学习助手命令行 demo。"""


from critic import review_answer
from planner import apply_review_result, choose_next_lesson, is_finished
from tools import add_history, load_state, save_state


def show_lesson(lesson):
    """打印当前课程内容。"""
    print(f"\n第 {lesson['id']} 课：{lesson['title']}")
    print(f"目标：{lesson['objective']}\n")
    for index, item in enumerate(lesson["content"], 1):
        print(f"{index}. {item}")
    print(f"\n练习：{lesson['exercise']}")


def run_once(state, answer, use_llm=None):
    """执行一轮学习、批改和状态更新。"""
    lesson = choose_next_lesson(state)
    result = review_answer(lesson, answer, use_llm=use_llm)
    apply_review_result(state, lesson, result)
    add_history(state, lesson["id"], result["passed"], result["feedback"])
    return result


def self_check():
    """运行最小自检，确认批改和状态推进可用。"""
    state = {
        "current_lesson": 1,
        "completed_lessons": [],
        "known_concepts": [],
        "weak_points": [],
        "history": [],
        "max_steps": 12,
    }
    result = run_once(
        state,
        "Agent 会围绕目标使用工具，根据状态和观察结果调整下一步。",
        use_llm=False,
    )
    assert result["passed"] is True
    assert state["current_lesson"] == 2
    assert state["completed_lessons"] == [1]
    print("self-check passed")


def main():
    """运行交互式学习循环。"""
    state = load_state()
    steps = 0


    print("AI Agent 学习助手 demo")
    print("输入 q 退出，状态会保存到 state.json。")


    while not is_finished(state) and steps < state.get("max_steps", 12):
        lesson = choose_next_lesson(state)
        show_lesson(lesson)
        answer = input("\n你的回答：").strip()
        if answer.lower() in {"q", "quit", "exit"}:
            break


        result = run_once(state, answer)
        save_state(state)
        steps += 1


        print("\n" + result["feedback"])
        print("批改方式：" + result.get("reviewer", "unknown"))
        if result["matched_keywords"]:
            print("命中关键词：" + "、".join(result["matched_keywords"]))


    if is_finished(state):
        print("\n已完成全部 demo 课程。")
    else:
        print("\n已保存进度，下次继续。")


if __name__ == "__main__":
    import sys


    if "--self-check" in sys.argv:
        self_check()
    else:
        main()
