#!/usr/bin/env python3
"""OpenAI API Client"""
import os, sys, argparse

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--prompt", "-p", required=True)
    p.add_argument("--model", "-m", default="gpt-4o-mini")
    p.add_argument("--stream", "-s", action="store_true")
    args = p.parse_args()
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY not set", file=sys.stderr)
        sys.exit(1)
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        r = client.chat.completions.create(
            model=args.model,
            messages=[{"role":"user","content":args.prompt}]
        )
        print(r.choices[0].message.content)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
