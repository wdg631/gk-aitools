#!/usr/bin/env python3
import sys

def count_tokens(text, provider="openai"):
    return len(text) // 4 if provider=="openai" else len(text) // 3

def estimate_cost(text, model="gpt-4o-mini"):
    rates = {"gpt-4o": 0.0025, "gpt-4o-mini": 0.00015, "claude-3-5-sonnet": 0.003}
    return count_tokens(text) / 1000 * rates.get(model, 0.00015)

if __name__ == "__main__":
    text = sys.stdin.read() if len(sys.argv)<2 else open(sys.argv[1]).read()
    t = count_tokens(text)
    print(f"Chars: {len(text)}, Tokens: {t}, Cost: ${estimate_cost(text):.6f}")
