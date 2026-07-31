# File Processing & Structured Data — Lecture Prep
**34-slide deck | Target: one 3-hour morning session | Fallback: split after CSV**

---

## Before you walk in

Files you need open/ready (terminal + editor), from this package:

| File | Used in |
|---|---|
| `demo/sample_scores.csv` | Live-build pipeline, between slide 31 and the lab |
| `data/messy_students.csv` | Lab Activity 1 (hand to students) |
| `data/enrollments.xml` | Lab Activity 2 (hand to students) |

Everything else below — the two crash demos and the pipeline — you type live, from an empty file, with students watching. Nothing is pre-written for those. The code blocks below are what to type, in order, not files to run.

---

## Timing plan (170 min teaching, 1 break) — and the checkpoint rule

| Section | Slides | Budget | Running total |
|---|---|---|---|
| Title + Roadmap | 1–2 | 5 min | 5 |
| File Basics | 3–6 | 15 min | 20 |
| Error Handling | 7–9 | 15 min | 35 |
| Paths & Encoding | 10–13 | 20 min | 55 |
| CSV Files | 14–18 | 25 min | **80** |
| **— CHECKPOINT —** | | | |
| *Break* | | 10 min | 90 |
| JSON Data | 19–23 | 20 min | 110 |
| XML Basics | 24–27 | 15 min | 125 |
| Validating Data | 28–30 | 15 min | 140 |
| Bridge slide | 31 | 5 min | 145 |
| Live pipeline build | (demo) | 15 min | 160 |
| Lab hand-off | 32 | 10 min | 170 |
| Takeaways/closing | 33–34 | — | push to next session if out of time |

**The checkpoint rule:** if you finish slide 18 (CSV quiz answer) later than the 90-minute mark, stop there for the break and **do not try to compress JSON/XML/Validation to catch up.** Pick up JSON at the start of session 2 instead. Rushing those three sections defeats the point of having them — validation in particular needs the slow walk-through, not a speed-run.

**If you must cut something on the day, cut in this order, not validation/error-handling:**
1. Slide 20's tuple→list JSON quirk — skip the slide, just say "JSON has no tuple type, so it becomes a list" out loud and move on.
2. Slide 25 (XML find/findall/iter) — fold its one key point into slide 24's wrap-up instead of running it as a separate slide.

---

## Slide-by-slide notes

### 1 — Title
Just framing. Don't linger.

### 2 — Session roadmap
Read the 8 cards as a flight path, not a list. One line each is enough — they'll see the detail later.

### 3 — Opening and closing files
- **Live-type:** open a file the unsafe way, `print(f.closed)` → False, then `f.close()`, then show `with` doing it automatically.
- **Likely question:** "what actually breaks if I forget close()?" → on a long-running program, too many open handles, or — bigger for them — data written with `'w'` mode that never gets flushed to disk before the program ends.

### 4 — Reading and writing text
- **Live-type:** `read()` vs looping line-by-line on the same file, show both give the same content, different memory behavior.
- Mention `\n` is the student's job on write — this trips people up constantly.

### 5–6 — Quick check / Answer (File Basics)
Let them answer before revealing. The "why" line is the actual lesson — read it out loud, don't just flash it.

### 7 — When file operations fail
- **Type this live, from empty, in front of them:**
  ```python
  with open('nonexistent_roster.txt') as f:
      data = f.read()
  ```
  Run it. It crashes. Let the red traceback sit on screen a few seconds — don't rush past it.
- Walk the traceback bottom-up out loud: "last line tells you what broke, line above tells you where."
- Then, in the same file, build the fix live:
  ```python
  try:
      with open('nonexistent_roster.txt') as f:
          data = f.read()
  except FileNotFoundError:
      print('File not found — check the path')
  ```
  Run again — handled, no crash.

### 8–9 — Quick check / Answer (Error Handling)
The contrast here is bare `except:` vs named exception — make sure they can articulate *why* bare except hides bugs, not just that it's "wrong."

### 10 — Working across platforms
- **Live-type:** `Path('data') / 'grades.csv'` on this machine; ask who's on Windows vs Mac and note the backslash/forward-slash difference would otherwise bite them.

### 11 — Text isn't just bytes
- Keep this conceptual — the code example is illustrative, don't over-focus on the specific string.
- **Likely question:** "how do I know what encoding a file uses?" → honest answer: you usually don't, until it breaks. UTF-8 is the safe default to assume and declare.

### 12–13 — Quick check / Answer (Paths & Encoding)
This is the one about relative paths breaking for a classmate — good moment to ask "has this happened to anyone already?" Most CS students have a war story.

### 14 — Reading and writing rows
- **Live-type:** open `data/messy_students.csv` (don't validate yet — just print raw rows) so they see what "messy" actually looks like before any cleanup talk.

### 15 — DictReader and DictWriter
- **Live-type:** same file with `DictReader`, show `row['name']` access.
- Worth showing live: print `row` for the line-13 (Tariq Mehmood) record — DictReader doesn't crash on the extra column, it silently adds a `{None: ['Lahore']}` entry. That's a genuinely surprising, concrete "messy data" moment — use it.

### 16 — Delimiters and a newline gotcha
- If anyone's on Windows, this is the slide to slow down on — it's the bug they're most likely to actually hit this semester.

### 17–18 — Quick check / Answer (CSV) — **checkpoint slide**
Check your clock here. See timing plan above.

---
### *(Break)*
---

### 19 — Reading and writing JSON
- **Live-type:** `json.dumps({...}, indent=2)` in a REPL so they see the formatting difference indent makes, before touching files.

### 20 — Nested data and type mapping
- Cut candidate #1 if behind schedule (see cut list above). If keeping it: the tuple→list line is the only thing that matters here — don't let the dict-of-lists example eat the clock.

### 21 — Safe access with .get()
- **Live-type:** trigger a real `KeyError` first (`s['gpa']` on a dict missing that key), then fix it with `.get()`. Mirrors the traceback-first approach from slide 7.

### 22–23 — Quick check / Answer (JSON)

### 24 — Elements, attributes, and ElementTree
- **Live-type:** open `data/enrollments.xml`, `ET.parse`, print `root.tag` and `root[0].attrib`.

### 25 — Searching the tree
- Cut candidate #2 if behind. If keeping it: the one thing they need is *why* `iter()` exists — direct-children-only vs. whole-tree search.
- **Live-type:** show `root.find('grade')` returning `None` on enrollment 104 (Hina Tariq) — real, not hypothetical, ties straight into validation later.

### 26–27 — Quick check / Answer (XML)

### 28 — Validating data on import
- **Type this live, from empty:**
  ```python
  scores = ['88', '91', 'absent', '79']
  total = 0
  for s in scores:
      total += int(s)
  print(total)
  ```
  Run it. It crashes on the third item — and **nothing prints**, because the loop dies before reaching `print(total)`. Point that silence out explicitly; it's the whole argument for validating row by row.
- Then build the fix live, in the same file:
  ```python
  scores = ['88', '91', 'absent', '79']
  total = 0
  for s in scores:
      try:
          total += int(s)
      except ValueError:
          print(f'skipping bad value: {s}')
  print(total)
  ```
  Run it — now it skips `'absent'`, prints the skip message, and still reaches the final total.

### 29–30 — Quick check / Answer (Validation)

### 31 — From files to databases
- Keep this short — it's a preview, not new content to test on. One line: "everything you validated today is exactly what a database table expects next time."

### Live pipeline build (between slide 31 and the lab)
Open `demo/sample_scores.csv` so it's visible, and start from an empty `.py` file. Build it up in these five steps, **running after each one** so students see the output change. Don't paste the final version — type it.

**Step 1 — read and print raw rows:**
```python
import csv

with open('sample_scores.csv', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row)
```
Run it. This is what "messy data" actually looks like — blank scores, `'abs'`, and one out-of-range `101`.

**Step 2 — add validation:**
```python
valid_rows = []
errors = []

with open('sample_scores.csv', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        name = row.get('name')
        raw_score = row.get('quiz_score')
        try:
            score = int(raw_score)
            valid_rows.append({'name': name, 'quiz_score': score})
        except ValueError as e:
            errors.append((row, str(e)))

print(f'{len(valid_rows)} ok, {len(errors)} bad')
```
Run it → `5 ok, 3 bad` (the two blank scores and `'abs'` get caught; `101` slides through because it's a valid integer).

**Step 3 — add the range check (a business rule, not just a type check):**
```python
        try:
            score = int(raw_score)
            if not (0 <= score <= 100):
                raise ValueError(f'out of range: {score}')
            valid_rows.append({'name': name, 'quiz_score': score})
        except ValueError as e:
            errors.append((row, str(e)))
```
Run it again → now `4 ok, 4 bad` — Faizan Riaz's `101` is correctly rejected too. Worth a beat here: "int() alone wouldn't have caught this. Validation isn't just type-checking."

**Step 4 — write the JSON output:**
```python
import json

with open('clean_scores.json', 'w', encoding='utf-8') as f:
    json.dump(valid_rows, f, indent=2)
```
Run it, then open `clean_scores.json` and show the pretty-printed result.

**Step 5 — write the CSV output:**
```python
with open('clean_scores.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['name', 'quiz_score'])
    writer.writeheader()
    writer.writerows(valid_rows)
```
Run it, open `clean_scores.csv` next to the JSON.

Close with: "the lab uses different data — GPAs and XML enrollments — but it's the exact same five-step pattern you just watched me type."

### 32 — Lab activities
- Hand out `data/messy_students.csv` for Activity 1, `data/enrollments.xml` for Activity 2.
- If time is short, assign Activity 1 in-class and Activity 2 as take-home / next-session work — don't split each activity in half.

### 33–34 — Takeaways / Closing
- If you've hit the time ceiling, skip live and just tell them to read these two slides themselves — they're summary, not new material.
