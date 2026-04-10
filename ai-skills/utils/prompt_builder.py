#!/usr/bin/env python3
def build_prompt(template, **kwargs):
    result = template
    for k, v in kwargs.items():
        result = result.replace("{{"+k+"}}", str(v))
    return result

SYSTEM = """You are a {{role}} assistant specializing in {{specialty}}.
Tone: {{tone}}. Format: {{format}}. Context: {{context}}."""

if __name__ == "__main__":
    print(build_prompt(SYSTEM,
        role="tech writer", specialty="AI tools",
        tone="friendly", format="markdown", context="developers"))
