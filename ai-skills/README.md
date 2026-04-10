# AI Skills

> 各类 AI 能力的快速调用工具，拿来即用

## 结构

```
ai-skills/
├── prompts/           # 55+ Prompt 模板
├── api-clients/      # OpenAI / Claude / Ollama 客户端
├── openclaw-skills/  # OpenClaw 技能定义
├── agents/          # AI Agent 配置
└── utils/          # Token 计数器 / 文本分割 / Prompt 构建
```

## 快速使用

```bash
# Claude 生成摘要
export ANTHROPIC_API_KEY=sk-ant-...
python ai-skills/api-clients/claude_client.py --prompt "Hello"

# 本地 Ollama
python ai-skills/api-clients/ollama_client.py --model llama3.2 --prompt "Hello"

# Token 计数
echo "hello world" | python ai-skills/utils/token_counter.py
```
