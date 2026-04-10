# AI API Clients

| Client | Model | Setup |
|--------|-------|-------|
| `openai_client.py` | GPT-4o / GPT-4o-mini | export OPENAI_API_KEY=sk-... |
| `claude_client.py` | Claude 3.5 Sonnet | export ANTHROPIC_API_KEY=sk-ant-... |
| `ollama_client.py` | Llama3.2 / Qwen (local) | ollama serve (no API key needed) |

```bash
python ai-skills/api-clients/openai_client.py -p "Hello" -m gpt-4o
python ai-skills/api-clients/claude_client.py -p "Hello"
python ai-skills/api-clients/ollama_client.py -p "Hello" -m llama3.2
```
