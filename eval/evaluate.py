"""Measure retrieval hit-rate (and optionally answer quality) on a question set.

Usage:
  python -m eval.evaluate --docs data --chunk-size 200 --k 4
  python -m eval.evaluate --docs data --chunk-size 100 --k 6 --answers
Edit eval/questions.json with 30-50 questions from YOUR notes. `keywords` are words/phrases a
correct answer must contain. Mark unanswerable questions with "out_of_scope": true.
"""
import argparse
import json
import pathlib

from rag.generate import NOT_FOUND, answer
from rag.ingest import chunk_pages, load_pdf
from rag.store import VectorStore

ap = argparse.ArgumentParser()
ap.add_argument("--docs", default="data")
ap.add_argument("--questions", default="eval/questions.json")
ap.add_argument("--chunk-size", type=int, default=200)
ap.add_argument("--k", type=int, default=4)
ap.add_argument("--answers", action="store_true", help="also call the LLM and score answers")
a = ap.parse_args()

pages = [p for f in sorted(pathlib.Path(a.docs).glob("*.pdf")) for p in load_pdf(str(f), f.name)]
store = VectorStore(chunk_pages(pages, size=a.chunk_size, overlap=a.chunk_size // 5))
qs = json.load(open(a.questions))

hit = ans_score = refused_ok = n_in = n_out = 0
for item in qs:
    hits = store.search(item["q"], k=a.k)
    if item.get("out_of_scope"):
        n_out += 1
        if a.answers:
            refused_ok += answer(item["q"], hits).strip() == NOT_FOUND
        continue
    n_in += 1
    text = " ".join(h["text"].lower() for h in hits)
    hit += any(kw.lower() in text for kw in item["keywords"])
    if a.answers:
        out = answer(item["q"], hits).lower()
        ans_score += sum(kw.lower() in out for kw in item["keywords"]) / max(len(item["keywords"]), 1)

print(f"chunk_size={a.chunk_size} k={a.k}")
print(f"Retrieval hit-rate: {hit}/{n_in} = {hit / max(n_in, 1):.0%}")
if a.answers:
    print(f"Answer keyword coverage: {ans_score / max(n_in, 1):.0%}")
    if n_out:
        print(f"Correctly refused out-of-scope: {refused_ok}/{n_out}")