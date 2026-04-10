#!/usr/bin/env python3
"""Claude API Client"""
import os, sys, argparse

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--prompt", "-p", required=True)
    p.add_argument("--model", "-m", default="claude-3-5-sonnet-20241022")
    args = p.parse_args()
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY not set", file=sys.stderr)
        sys.exit(1)
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)
        r = client.messages.create(
            model=args.model,
            max_tokens=4096,
            messages=[{"role":"user","content":args.prompt}]
        )
        print(r.content[0].text)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
