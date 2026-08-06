# AI-learning-demo

一个最小 AI Agent 学习助手 demo。

## 运行

```powershell
python main.py
```

## 自检

```powershell
python main.py --self-check
```

## 可选：启用模型批改

默认使用本地关键词规则批改，不需要安装依赖。

如需用 OpenAI 批改，设置环境变量后运行：

```powershell
$env:OPENAI_API_KEY = "你的 key"
$env:OPENAI_MODEL = "gpt-4.1-mini"
python main.py
```

没有 `OPENAI_API_KEY` 或模型调用失败时，会自动回退到关键词批改。
