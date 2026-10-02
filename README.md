# VEX IQ Vocab

A bilingual (English / Simplified Chinese) vocabulary list and sentence-frame bank for middle-school VEX IQ robotics, built to be the single source for flashcards, Kahoots, handouts and other classroom materials.

> **Status: planning.** See [PLAN.md](PLAN.md) for decisions, the data spec and the roadmap.

## What's here (planned)

- `data/vocab.csv` — terms across building, coding, engineering, design process, competition and the current season game.
- `data/frames.csv` — sentence frames for planning, collaboration, driving, judge interviews and talking to referees.
- `images/` — one photo per term, named by ID (`BLD-023.png`).
- `schema.yaml` + `validate.py` — column rules, checked automatically on every push.

## Rules for humans and AI tools

1. **The CSVs in `data/` are the source of truth.** Edit them directly; never edit generated output.
2. **English is the target.** Students should use the English terms. Chinese (`zh`) is support only.
3. **Chinese appears in reference materials, never in review materials** (quizzes, flashcards, Kahoots).
4. **`short_def` must stand on its own in simple English, ≤ 75 characters.**
5. **IDs are permanent.** Never reuse or renumber.
6. **Chinese translations:** official VEX Chinese terms first, then established community terms, literal translation last.
7. **VEX IQ only.** Don't import VRC/V5 terms that don't apply.
8. **No student data** — this repo is public.
9. Run `python validate.py` before committing.
