"""AI Agent 学习课程内容。"""


LESSONS = [
    {
        "id": 1,
        "title": "Agent、LLM Call 和 Workflow 的区别",
        "objective": "能判断一个任务更像普通模型调用、固定工作流还是 Agent。",
        "content": [
            "LLM Call 主要是一次输入对应一次输出。",
            "Workflow 按固定步骤执行，流程通常提前写死。",
            "Agent 围绕目标维护状态，并根据观察结果决定下一步动作。",
        ],
        "exercise": "为什么竞品调研通常比文章总结更像 Agent 任务？",
        "keywords": ["目标", "工具", "状态", "下一步", "调整"],
        "weak_point": "agent_definition",
    },
    {
        "id": 2,
        "title": "Agent 执行循环",
        "objective": "理解 Plan -> Act -> Observe -> Reflect 的基本闭环。",
        "content": [
            "Planner 根据目标和状态决定下一步。",
            "Executor 调用工具并返回 observation。",
            "Agent 根据 observation 更新 state，再决定继续还是结束。",
        ],
        "exercise": "请用一句话解释为什么 Agent 需要 observation。",
        "keywords": ["结果", "观察", "状态", "调整", "下一步"],
        "weak_point": "agent_loop",
    },
    {
        "id": 3,
        "title": "State 状态设计",
        "objective": "能设计一个保存目标、进度、证据和缺口的最小 state。",
        "content": [
            "State 不是聊天记录，而是 Agent 决策依据。",
            "最小 state 通常包含 goal、progress、evidence、missing 和 weak_points。",
            "事实、推断和草稿最好分开保存，避免记忆污染。",
        ],
        "exercise": "一个调研 Agent 的 state 里为什么要有 missing 字段？",
        "keywords": ["缺口", "信息", "下一步", "重复", "完成"],
        "weak_point": "state_design",
    },
    {
        "id": 4,
        "title": "Critic 自我检查",
        "objective": "理解 Critic 如何根据标准发现答案或产物的问题。",
        "content": [
            "Critic 不负责执行工具，负责按标准挑错。",
            "好的 Critic 要有明确检查项，不能只问“好不好”。",
            "检查结果应该能转化成下一步动作。",
        ],
        "exercise": "为什么 Critic 的检查标准要写得具体？",
        "keywords": ["标准", "证据", "缺少", "修正", "通过"],
        "weak_point": "critic",
    },
]


def get_lesson(lesson_id):
    """按课程 id 返回课程；不存在时返回 None。"""
    return next((lesson for lesson in LESSONS if lesson["id"] == lesson_id), None)


def first_lesson_id():
    """返回第一课 id。"""
    return LESSONS[0]["id"]


def last_lesson_id():
    """返回最后一课 id。"""
    return LESSONS[-1]["id"]
