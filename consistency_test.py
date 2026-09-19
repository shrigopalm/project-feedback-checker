"""Checks how consistent the model is.

Sends every test case to the model several times and reports how often the
score is the same. If a case has low agreement, look at it first.

Run:  python consistency_test.py        (RUNS=5 by default)
Mock: USE_MOCK=1 python consistency_test.py
"""
import json
import os
from collections import Counter

from llm import get_feedback

RUNS = int(os.getenv("RUNS", "5"))


def load_cases():
    with open("test_cases.json", encoding="utf-8") as f:
        cases = json.load(f)
    # A very long input, to see what happens when text gets cut off
    long_text = "I built a small Python tool that sorts my notes by topic. " * 200
    cases.append({"name": "very long", "text": long_text})
    return cases


def main():
    rows = []
    for case in load_cases():
        scores = [get_feedback(case["text"])["score"] for _ in range(RUNS)]
        top_score, top_count = Counter(scores).most_common(1)[0]
        rows.append((case["name"], scores, top_count / RUNS))

    print(f"{'case':<22}{'scores':<24}agreement")
    for name, scores, agreement in rows:
        print(f"{name:<22}{str(scores):<24}{agreement:.0%}")
    average = sum(r[2] for r in rows) / len(rows)
    print(f"\nAverage agreement across {len(rows)} cases: {average:.0%}")

    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(
            [{"case": n, "scores": s, "agreement": a} for n, s, a in rows],
            f, indent=2,
        )


if __name__ == "__main__":
    main()
