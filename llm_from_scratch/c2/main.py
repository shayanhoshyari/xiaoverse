from pathlib import Path

VERDICT = Path(__file__).with_name("the-verdict.txt")

with open(VERDICT, "r", encoding="utf-8") as f:
    raw_text = f.read()

print("Total number of character:", len(raw_text))
print(raw_text[:99])
