#!/usr/bin/env python3
def split_by_chars(text, chunk_size=2000, overlap=100):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size-overlap)]

def split_by_sentences(text, max_tokens=2000):
    sents = text.replace(chr(10), " ").split(".")
    chunks, cur = [], ""
    for s in sents:
        if len(cur)+len(s) < max_tokens*4:
            cur += s + "."
        else:
            if cur: chunks.append(cur)
            cur = s + "."
    if cur: chunks.append(cur)
    return chunks

if __name__ == "__main__":
    import sys
    text = sys.stdin.read() if len(sys.argv)<2 else open(sys.argv[1]).read()
    for i, c in enumerate(split_by_sentences(text)):
        print(f"--- Chunk {i+1} ---", c[:200])
