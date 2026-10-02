# VEX IQ Vocab — Project Plan

Status: **seeding** — Building (BLD) and Coding (CODE) drafted; ENG, EDP, COMP, SEASON to come. This file records decisions and the spec. Update it when a decision changes.

## 1. Purpose

Students should become experts in the VEX IQ system — to learn engineering and compete well, but also to learn that **deliberately building expertise is a ratchet towards mastery**. At the middle-school level this is heavily scaffolded, and a shared vocabulary is the central tool.

Audience:
- **Students** — mostly Mandarin L1; a few Cantonese at home (all with decent English). English is the language of instruction for robotics; English levels vary widely.
- **Parents** — reference materials help them see robotics as a real class.
- **AI tools** — most building and generating work will be done with AI tools, so the data and its rules must be self-explanatory.

Goal: students **use the English terms**. Chinese is a support for understanding, not a replacement.

## 2. Decisions

| Topic | Decision |
|---|---|
| Storage | CSV files in a public GitHub repo. No database, no spreadsheet file. |
| Source of truth | `data/*.csv` — edited directly (VS Code + *Edit CSV* / *Rainbow CSV*, or via AI tools). Never generated. |
| Validation | `schema.yaml` defines columns and allowed values; `validate.py` checks the CSVs; a GitHub Action runs it on every push. |
| Encoding | UTF-8, no BOM, comma-separated, `\n` line endings. Validator rejects anything else. |
| Lists inside a cell | Semicolon-separated (`drivetrain; coding`). |
| Chinese | Simplified only. Official VEX Chinese terms first; then terms used by the Chinese VEX community; literal translation last. One `zh` column, no notes column. |
| Chinese in outputs | Shown in **reference** materials (glossaries, handouts, parent sheets). Hidden in **review** materials (Kahoot, flashcards, quizzes). |
| Programming languages | VEXcode IQ **Blocks + Python**. No C++ for now. |
| Coding scope | ~105 terms in three tiers: (1) categories, devices, block types; (2) the words inside commands; (3) programming concepts. Not every block: `ref_url` points to the full VEX reference. 2nd-gen sensors only; AI Vision Sensor included. |
| Coding Chinese | From **VEXcode IQ's own Chinese interface** (the block text students see), not the machine-translated Chinese API site, which is unreliable (e.g. Motors → 汽车). VEXcode uses some unusual terms (heading = 归位角度, rotation = 转向); we follow VEXcode and mention alternatives in `explanation`. |
| Block pictures | The `blocks` column holds block text in [scratchblocks](https://scratchblocks.github.io/) syntax, as used on VEX's reference site (e.g. `drive [forward v] for (200) [mm v] ▶`). The app draws it; no screenshots. scratchblocks is vendored in `app/vendor/` (MIT). |
| Links | `ref_url`: one "learn more" link per term — VEX API reference section for CODE, VEX Library article for BLD. |
| Coding scope | Not every block. Devices, block categories, the words inside commands, and concepts. |
| Building scope | Part *families* (beam, plate, pin…) with notes on how sizes/types are described — not every size. Grouped by VEX's own kit categories. |
| Images | Concept images must not show the term's own name (it would give away quiz answers). Separate files in `images/`, named by ID (`BLD-023.png`), square PNG on white, ≤ ~200 KB. VEX images are used for now (cropped from the kit poster, or store photos), credited in `images/CREDITS.md`; own photos can replace them under the same filename. Check with `python3 tools/contact_sheet.py`. |
| IDs | Permanent. Never reused or renumbered; retired IDs stay retired. |
| Overlapping terms | One primary `domain` + free `tags`. If a term means different things in different domains (e.g. drivetrain the mechanism vs. Drivetrain the VEXcode device), it gets **two rows**. |
| Sentence frames | Separate CSV in the same repo, linked to vocab by ID. |
| Blocks vs Python | Same meaning, different syntax → **one row**, with the `blocks` and `python` columns. Terms that exist in only one language (indentation, `def`, `import`, hat block, My Blocks) get their own row, tagged `python` or `blocks`. |
| Mirroring for China | Later (Gitee). Student-facing apps should bundle a data snapshot rather than fetch from GitHub live. |
| Privacy | Repo is public: no student names or data, ever. |

## 3. Repo layout (target)

```
vex-iq-vocab/
  README.md          ← what this is + rules for humans and AI tools
  PLAN.md            ← this file
  schema.yaml        ← column definitions + allowed values
  validate.py        ← checks data/ against schema.yaml
  data/
    vocab.csv
    frames.csv
  images/            ← <ID>.png, extras as <ID>-a.png, <ID>-b.png
  sources/           ← reference data pulled from VEX sources (not validated, not edited by hand)
  tools/             ← generators (Kahoot, flashcards, handouts…)
  .github/workflows/validate.yml
```

## 4. `data/vocab.csv` columns

| Column | Required | Notes |
|---|---|---|
| `id` | yes | `<PREFIX>-<3 digits>`, e.g. `BLD-023`. Prefix matches domain. |
| `term_en` | yes | The English term students should use. |
| `aka` | | Other names / abbreviations, `;`-separated (e.g. `DR4B; double reverse four-bar`). |
| `zh` | yes* | Simplified Chinese. *Required before status `verified`. |
| `short_def` | yes | Simple English, **≤ 75 characters** (Kahoot answer limit). Must make sense without Chinese. |
| `explanation` | | Longer explanation for reference handouts. |
| `example` | | Example sentence using the term in context. |
| `confused_with` | | IDs of commonly confused terms, `;`-separated. Used as quiz distractors. |
| `blocks` | | CODE only: block text in scratchblocks syntax (as on api.vex.com), drawn by the app. |
| `python` | | CODE only: VEXcode IQ Python equivalent. |
| `domain` | yes | One of the domains below. |
| `subdomain` | yes | Allowed values per domain (see below). |
| `tags` | | Free tags, `;`-separated, for cross-listing. |
| `level` | yes | 1 = everyone, 2 = role-specific (builders / coders / drivers), 3 = expert. |
| `season` | | SEASON domain only, e.g. `2026-27`. |
| `image` | | Filename in `images/`, or blank if none yet. |
| `ref_url` | | One https link to learn more: VEX API reference (CODE), VEX Library article (BLD), game manual (COMP/SEASON). |
| `store_skus` | | BLD only: vexstore.cn SKUs that contain this part, `;`-separated, for re-ordering. Must exist in `sources/vexstore-cn-iq-parts.csv`. Usually packs, so one SKU can cover several parts and one part can come in several SKUs. |
| `status` | yes | `draft` → `reviewed` → `verified`. |

## 5. Domains

Subdomains are provisional — verify against the VEX IQ kit poster and VEXcode IQ before seeding. The allowed values live in `schema.yaml`; change them there.

| Prefix | Domain | Covers | Provisional subdomains |
|---|---|---|---|
| `BLD` | Building | Physical parts: competition kit + extensions we actually use (e.g. pneumatics) | general, electronics, specialty, shafts, connectors, pins-standoffs, wheels, beams-plates, gears, sprockets-chain, cams, linear-motion, pneumatics — **confirmed**: Competition Kit poster categories + `general` (size/naming words) + `pneumatics` |
| `CODE` | Coding | VEXcode IQ: devices, block categories, command words, programming concepts | basics, drivetrain, motion, sensing, vision, controller, screen-console, events, control, operators, variables, functions, python, concepts — **confirmed**, follows VEXcode's categories |
| `ENG` | Engineering | Mechanisms and design/control techniques: intake, DR4B, cascade lift, arm, claw, catapult, drivetrain (mechanism), gear ratio, torque, autonomous routine, PID… | mechanisms, drivetrains, mechanical-concepts, control-techniques |
| `EDP` | Design process | Engineering design process + engineering notebook + judge interview vocabulary | process, notebook, interview |
| `COMP` | Competition | Season-independent: coach, referee, match, Teamwork Challenge, Driver/Autonomous Coding Skills, scrimmage, regionals, nationals, Worlds… | events, roles, matches, rules, awards |
| `SEASON` | Season game | This year's game elements and scoring. Tagged with `season` so they can be retired. | game-elements, scoring, field |

VEX IQ note: Teamwork Challenge is **cooperative** (two teams working together), not opposing alliances. Avoid VRC/V5 terms that don't apply to IQ.

## 6. `data/frames.csv` columns

| Column | Required | Notes |
|---|---|---|
| `id` | yes | `FRM-<3 digits>` |
| `situation` | yes | `planning`, `building`, `coding`, `driving`, `scouting`, `interview`, `referee`, `notebook` |
| `function` | yes | `agree`, `disagree`, `propose`, `ask-for-help`, `explain`, `clarify`, `report`… |
| `frame_en` | yes | With blanks: `I think we should ___ because ___.` |
| `zh` | yes* | Simplified Chinese. |
| `example` | | Frame filled in. |
| `level` | yes | 1–3, as above. |
| `vocab_ids` | | Related vocab IDs, `;`-separated. |
| `notes` | | Norms, e.g. for `referee`: students speak for themselves, calmly, after the match. |
| `status` | yes | `draft` → `reviewed` → `verified`. |

## 7. Validation rules (`validate.py`)

- UTF-8 without BOM, LF line endings; header row matches schema exactly.
- No leading/trailing spaces in cells.
- `id` unique, correct format, prefix matches `domain`.
- Required columns non-empty (respecting `status` for `zh`).
- `domain`, `subdomain`, `level`, `status`, `situation`, `function` in allowed lists — with "did you mean…" suggestions.
- `short_def` ≤ 75 characters.
- Every ID in `confused_with` / `vocab_ids` exists.
- Every `image` file exists in `images/`.
- `blocks` / `python` only on CODE rows; `season` only on SEASON rows.
- Warnings (not errors): images in `images/` with no matching row; `verified` rows missing `example`.

## 8. Planned outputs

- Kahoot import sheets (by domain / level / subdomain) — `short_def` + image, distractors from `confused_with`, no Chinese.
- Printable flashcards — English front, definition + image back, no Chinese.
- Reference glossaries / handouts — English + Chinese + explanation.
- Parent glossary.
- Sentence-frame cards by situation.
- Image contact sheet for checking photos against IDs.

## 9. Roadmap

- [x] **0. Plan** — this document; public GitHub repo created.
- [x] **1. Scaffold** — `schema.yaml`, `validate.py`, GitHub Action, empty CSVs with headers, README rules for AI tools.
- [ ] **2. Confirm taxonomy** — ~~VEX kit poster categories~~ (done); VEXcode IQ block categories; level definitions.
- [ ] **3. Seed vocab** — AI-drafted, ~250–300 terms, all `status=draft`. One domain at a time, teacher review per domain.
  - [x] BLD — 76 terms (part families from the Competition Kit poster + pneumatics + Smart Motor Mount + Inertial Sensor), all 76 with images (BLD-001–005 are diagrams from `tools/diagrams.py`)
  - [x] CODE — 106 terms (Blocks + Python), VEXcode Chinese, all with reference links; every term has a block drawing or an image
  - [ ] ENG · EDP · COMP · SEASON
- [ ] **4. Seed frames** — starter set across all situations.
- [ ] **5. Chinese review** — check `zh` against official VEX Chinese materials; promote to `reviewed`/`verified`.
- [ ] **6. Images** — BLD done from VEX sources; other domains to come. Optional: replace with own photos (student project).
- [ ] **7. Generators** — Kahoot, flashcards, handouts. ~~Contact sheet~~ (`tools/contact_sheet.py`). ~~Browser app proof of concept~~ (`app/index.html`).
- [ ] **8. China access** — Gitee mirror.

## 10. Sources

| Source | Used for |
|---|---|
| [VEX IQ Competition Kit poster (PDF)](https://content.vexrobotics.com/vexpro/pdf/IQ-Competition-Kit-111521.pdf) | BLD subdomains and English part names |
| [VEX IQ (2nd gen) API reference](https://api.vex.com/iq2/home/index.html) | CODE terms, block text, Python names, `ref_url`s. The site publishes `/iq2/searchindex.js` (every page + section anchor) and `/iq2/_sources/<page>.md.txt` (raw page source). Both must be fetched from a browser on that site (bot protection blocks scripts). |
| VEXcode IQ Chinese UI text | CODE `zh`. Loaded by the reference site's block renderer: `/assets/scratchblocks/translations-all.js` → language `zh_cn` (keys like `iq2DriveFor`, `brakeTypeHold`, plus `dropdowns` and `palette`). |
| [VEX Library](https://kb.vex.com/hc/en-us) | BLD `ref_url`s. Search with `/api/v2/help_center/articles/search.json?query=…` from a browser on kb.vex.com. |
| [vexstore.cn IQ products](https://www.vexstore.cn/iq?vex_classroom=IQ) | Official Chinese part names → `sources/vexstore-cn-iq-parts.csv`. Pulled from the store's public search index (Algolia), which returns every IQ product with its Chinese name and pack contents in one request. Re-pull the same way when the catalog changes. |

## 11. Open questions

- Level definitions: is "role-specific" the right meaning for level 2?
- Exact VEX IQ kit categories and which extension kits to include beyond pneumatics.
- Current season game name and elements (for SEASON domain).
- Who reviews the Chinese?
- Content license (e.g. CC BY-NC-SA 4.0) — matters if other teachers reuse it.
