# VEX IQ Vocab

A bilingual (English / Simplified Chinese) vocabulary list and sentence-frame bank for middle-school VEX IQ robotics, built to be the single source for flashcards, Kahoots, handouts and other classroom materials.

> **Status: scaffolded, not yet seeded.** See [PLAN.md](PLAN.md) for decisions, the data spec and the roadmap.

## What's here

- `data/vocab.csv` — terms across building, coding, engineering, design process, competition and the current season game.
- `data/frames.csv` — sentence frames for planning, collaboration, driving, judge interviews and talking to referees.
- `images/` — one photo per term, named by ID (`BLD-023.png`).
- `schema.yaml` + `validate.py` — column rules, checked automatically on every push.

## Browse the list

**Online:** https://insufficientdoubt.github.io/vex-iq-vocab/ (GitHub Pages, updates a minute or two after each push).

`app/index.html` is a simple browser for the vocab list: an index by domain and subdomain, search (English or 中文), and a page per term. It reads `data/vocab.csv` directly, so it always shows the current data. To run it locally it needs a web server, not a double-click:

```
python3 -m http.server 8000
```

then open http://localhost:8000/app/

`app/lessons.html` is a teacher reference: the vocab grouped by the VEX IQ STEM Lab lesson that first teaches each term (`stem_lab` column), in VEX's suggested pacing order. It isn't linked from the student app.

## Rules for humans and AI tools

1. **The CSVs in `data/` are the source of truth.** Edit them directly; never edit generated output.
2. **English is the target.** Students should use the English terms. Chinese (`zh`) is support only.
3. **Chinese appears in reference materials, never in review materials** (quizzes, flashcards, Kahoots).
4. **`short_def` must stand on its own in simple English, ≤ 75 characters.**
5. **IDs are permanent.** Never reuse or renumber.
6. **Chinese translations:** official VEX Chinese terms first (store names for parts, VEXcode's Chinese interface for coding), then established community terms, literal translation last. Don't use the machine-translated Chinese on api.vex.com.
7. **VEX IQ only.** Don't import VRC/V5 terms that don't apply.
   **Sources: VEX first.** Use VEX IQ materials (VEX Library, IQ STEM Labs, Hero Bot articles) for terms, grouping and wording, then VEX EXP/V5 articles when the idea carries over to IQ. A term VEX doesn't cover may come from a community source (e.g. Purdue SIGBots wiki), but only as level 3 with tags `advanced; community-sourced`.
8. **No student data** — this repo is public.
9. Run `python3 validate.py` before committing (needs `pip install pyyaml`). GitHub runs it on every push too.
10. `blocks` uses scratchblocks syntax, copied from VEX's API reference where possible.
11. Allowed domains, subdomains, levels and statuses live in `schema.yaml` — change them there.
