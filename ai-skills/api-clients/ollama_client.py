#!/usr/bin/env python3
"""Ollama Local Model Client"""
import os, sys, argparse, urllib.request, json

OLLAMA_URL = "http://localhost:11434/api/generate"

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--prompt", "-p", required=True)
    p.add_argument("--model", "-m", default="llama3.2")
    p.add_argument("--stream", "-s", action="store_true")
    args = p.parse_args()
    data = json.dumps({
        "model": args.model,
        "prompt": args.prompt,
        "stream": args.stream
    }).encode()
    req = urllib.request.Request(
        OLLAMA_URL, data=data,
        headers={"Content-Type":"application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read())
            print(result.get("response",""))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
