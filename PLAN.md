# VEX IQ Vocab — Project Plan

Status: **seeding** — Building (77), Coding (107) and Engineering (72) drafted, plus a first set of EDP (12) and COMP (13) terms; all `status=draft`. SEASON and sentence frames to come. Live app: https://insufficientdoubt.github.io/vex-iq-vocab/

This file records decisions, the spec, and how the work was done (§12). Update it when a decision changes. **New AI session? Read §12 first.**

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
| Block pictures | The `blocks` column holds block text in [scratchblocks](https://scratchblocks.github.io/) syntax, as used on VEX's reference site (e.g. `drive [forward v] for (200) [mm v] ▶`). Multi-line scripts are allowed (newlines inside the quoted cell; C blocks end with `end`). The app draws it; no screenshots. scratchblocks is vendored in `app/vendor/` (MIT). A CODE term needs either an `image` or `blocks`; the card shows the image if both. |
| Links | `ref_url`: one "learn more" link per term — VEX API reference section for CODE, VEX Library article for BLD. |
| Sources | **VEX first**, for content *and* grouping: VEX IQ materials (VEX Library, IQ STEM Labs and their Lesson Summaries, Hero Bot articles) → VEX EXP/V5 articles when the idea carries over to IQ → community sources only for terms VEX doesn't cover. Community-sourced terms are always level 3 and tagged `advanced; community-sourced`; their `ref_url` points to the community source. |
| Engineering scope | Mechanisms and concepts, not parts: don't repeat a part BLD already has (omni wheel, flywheel, tank tread…) or a concept CODE already has (torque CODE-037, velocity CODE-021, motor group CODE-031); link to them with `confused_with` or in `explanation`. Gear ratio is explained as done with gears or sprockets (no pulleys). Controller drive modes (tank/arcade) are in ENG, tagged `controller`. |
| Teaching order | `stem_lab` records where VEX's IQ (2nd gen) STEM Labs first teach a term, as `<unit>.<lesson>`. Units are numbered in the order of VEX's Cumulative Pacing Guide (the 36-, 24- and 14-week plans all use it): 1 Tug of War, 2 Team Freeze Tag, 3 Robot Soccer, 4 Cube Collector, 5 Up and Over, 6 Treasure Hunt, 7 Castle Crasher, 8 Competition 101 (current season, now VEX IQ Level Up). This is a *suggested* order (VEX says units can be used in different sequences), and it differs from the order VEX's catalog lists them in. Only a term the lesson actually teaches (defines, explains or lists in its concepts) counts, not every part used in a build. If several lessons teach it, use the earliest in pacing order. Use it with `level` to decide when to introduce a term. Teacher reference only: not shown in the student app; `app/lessons.html` lists terms by lesson. |
| Building scope | Part *families* (beam, plate, pin…) with notes on how sizes/types are described — not every size. Grouped by VEX's own kit categories. |
| Images | Concept images must not show the term's own name (it would give away quiz answers) — applies to new images; the five BLD diagrams (BLD-001–005) keep their labels by decision, and VEXcode screenshots may show real button labels. Separate files in `images/`, named by ID (`BLD-023.png`), square PNG on white, ≤ ~200 KB. VEX images are used for now (cropped from the kit poster, or store photos), credited in `images/CREDITS.md`; own photos can replace them under the same filename. Check with `python3 tools/contact_sheet.py`. |
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
  tools/             ← diagrams.py (draws concept images), contact_sheet.py; later: Kahoot, flashcards, handouts
  app/               ← index.html (student-facing browser app, served on GitHub Pages), lessons.html (teacher reference: vocab by STEM Lab lesson, not linked from the app), vendor/scratchblocks.min.js
  index.html, .nojekyll  ← GitHub Pages: root redirects to app/
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
| `ref_url` | | One https link to learn more: VEX API reference (CODE), VEX Library article (BLD, ENG), VEX IQ STEM Lab page (ENG/EDP/COMP), game manual (COMP/SEASON). Non-VEX links only on `community-sourced` rows. |
| `stem_lab` | | `<unit>.<lesson>` (e.g. `1.3`) of the VEX IQ (2nd gen) STEM Lab lesson that first **teaches** the term. Must exist in `sources/iq-stem-labs.csv`, which holds the unit/lesson names, concepts and links. Blank if no lab teaches it. |
| `store_skus` | | BLD only: vexstore.cn SKUs that contain this part, `;`-separated, for re-ordering. Must exist in `sources/vexstore-cn-iq-parts.csv`. Usually packs, so one SKU can cover several parts and one part can come in several SKUs. |
| `status` | yes | `draft` → `reviewed` → `verified`. |

## 5. Domains

BLD, CODE and ENG subdomains are confirmed; EDP/COMP/SEASON are provisional — confirm with the teacher before seeding. The allowed values live in `schema.yaml`; change them there (the app's sidebar order = order of first appearance in the CSV; display names for hyphenated subdomains are in `SUB_NAMES` in `app/index.html`).

| Prefix | Domain | Covers | Provisional subdomains |
|---|---|---|---|
| `BLD` | Building | Physical parts: competition kit + extensions we actually use (e.g. pneumatics) | general, electronics, specialty, shafts, connectors, pins-standoffs, wheels, beams-plates, gears, sprockets-chain, cams, linear-motion, pneumatics — **confirmed**: Competition Kit poster categories + `general` (size/naming words) + `pneumatics` |
| `CODE` | Coding | VEXcode IQ: devices, block categories, command words, programming concepts | basics, drivetrain, motion, sensing, vision, controller, screen-console, events, control, operators, variables, functions, python, concepts — **confirmed**, follows VEXcode's categories |
| `ENG` | Engineering | Mechanisms, mechanical concepts and driving/control techniques: drivetrain types, manipulators (arms, claws, intakes, lifts, launchers), gear ratio, force, center of mass, autonomous, path planning, PID… | drivetrains, manipulators, power-transfer, forces, control-techniques — **confirmed**: follows the VEX Library IQ Mechanical articles (drivetrains, assemblies, motion) and the IQ STEM Lab concepts (force, mechanical advantage, center of mass, path planning) |
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
- [ ] **2. Confirm taxonomy** — ~~VEX kit poster categories~~, ~~VEXcode IQ categories~~ (done); level definitions; ENG/EDP/COMP/SEASON subdomains.
- [ ] **3. Seed vocab** — AI-drafted, ~250–300 terms, all `status=draft`. One domain at a time, teacher review per domain.
  - [x] BLD — 77 terms (part families from the Competition Kit poster + pneumatics + Smart Motor Mount + Inertial Sensor + AI Vision Sensor), all with images, store SKUs and VEX Library links (BLD-001–005 are diagrams from `tools/diagrams.py`)
  - [x] CODE — 107 terms (Blocks + Python), VEXcode Chinese, all with reference links; every term has a block drawing or an image
  - [x] ENG — 72 terms from VEX IQ sources (6 community-sourced, level 3), all with images.
  - [x] `stem_lab` — 80 terms across all domains mapped to the STEM Lab lesson that first teaches them (from every lesson's Lesson Summary PDF).
  - [ ] EDP · COMP — first terms added as they came up in the VEX IQ sources (12 EDP, 13 COMP, all with images). **Still to do:** evaluate both domains as a whole and add what's missing from other sources (game manual, RECF judge guide and notebook rubric, Competition 101 STEM Labs…).
  - [ ] SEASON
- [ ] **4. Seed frames** — starter set across all situations.
- [ ] **5. Chinese review** — check `zh` against official VEX Chinese materials; promote to `reviewed`/`verified`.
- [x] **6. Images** — every term has a picture (BLD, CODE, ENG, EDP, COMP). VEX images credited in `images/CREDITS.md`; concept diagrams in `tools/diagrams.py`. SEASON to come with that domain. Optional: replace with own photos (student project).
- [ ] **7. Generators** — Kahoot, flashcards, handouts. ~~Contact sheet~~ (`tools/contact_sheet.py`). ~~Browser app proof of concept~~ (`app/index.html`).
- [ ] **8. China access** — Gitee mirror.

## 10. Sources

| Source | Used for |
|---|---|
| [VEX IQ Competition Kit poster (PDF)](https://content.vexrobotics.com/vexpro/pdf/IQ-Competition-Kit-111521.pdf) | BLD subdomains and English part names |
| [VEX IQ (2nd gen) API reference](https://api.vex.com/iq2/home/index.html) | CODE terms, block text, Python names, `ref_url`s. The site publishes `/iq2/searchindex.js` (every page + section anchor) and `/iq2/_sources/<page>.md.txt` (raw page source). Both must be fetched from a browser on that site (bot protection blocks scripts). |
| VEXcode IQ Chinese UI text | CODE `zh`. Loaded by the reference site's block renderer: `/assets/scratchblocks/translations-all.js` → language `zh_cn` (keys like `iq2DriveFor`, `brakeTypeHold`, plus `dropdowns` and `palette`). |
| [VEX Library](https://kb.vex.com/hc/en-us) | BLD and ENG `ref_url`s; ENG terms and grouping (IQ › Mechanical: drivetrains, assemblies, arms, claws, gears/sprockets, wheels, motor groups; Competition Robots: Hero Bots). Search with `/api/v2/help_center/articles/search.json?query=…` from a browser on kb.vex.com; list a whole category with `/api/v2/help_center/en-us/categories/<id>/articles.json` (IQ = 360002324792). |
| [VEX IQ STEM Labs](https://education.vex.com/stemlabs/iq) | ENG/EDP/COMP definitions. The KB article "IQ (2nd gen) STEM Lab Unit Concepts" maps every unit to its concepts. Each lesson's *Learn* page links a **Lesson Summary PDF** on content.vexrobotics.com with VEX's kid-level definitions (force, traction, gear train, mechanical advantage, center of mass, manipulator, intake, claw, scouting, path planning, autonomous…); the PDFs download fine with curl. education.vex.com itself needs the browser. Competition 101 (VEX IQ Level Up) has the event vocabulary. |
| [VEX IQ Cumulative Pacing Guide](https://docs.google.com/spreadsheets/d/1QmNfN8X9Trpr8UhcZAGPa-akSaPDrFxsoluerQ0AMQk) | STEM Lab unit order for `stem_lab` → `sources/iq-stem-labs.csv`. A Google Sheet, so each tab exports with `/export?format=csv&gid=<tab id>` (curl works). The link.vex.com download links are blocked to scripts. |
| [Purdue SIGBots wiki](https://wiki.purduesigbots.com) | Community source, only for level-3 terms VEX doesn't cover (bang-bang, PID, proportional control, setpoint, error, odometry). curl works. Alternative for PID: George Gillard, *An Introduction to PID Controllers*. |
| [vexstore.cn IQ products](https://www.vexstore.cn/iq?vex_classroom=IQ) | Official Chinese part names → `sources/vexstore-cn-iq-parts.csv`. Pulled from the store's public search index (Algolia), which returns every IQ product with its Chinese name and pack contents in one request. Re-pull the same way when the catalog changes. |

## 11. Open questions

- Level definitions: is "role-specific" the right meaning for level 2?
- Which extension kits beyond pneumatics (currently: pneumatics, Smart Motor Mount, AI Vision Sensor; skipped: hybrid/bevel/crown/differential gears, pulleys, turntables).
- Current season game name and elements (for SEASON domain).
- Who reviews the Chinese?
- Content license (e.g. CC BY-NC-SA 4.0) — matters if other teachers reuse it.
- EDP and COMP: evaluate holistically before calling them done — the current terms are only the ones that came up in the VEX IQ engineering sources. Check against the game manual, RECF judging materials and the notebook rubric.
- ENG Chinese is all unofficial (no VEX Chinese source found for mechanism names): check especially 操作机构, 被动/主动机构, 搜集器 (intake, from the store's Intake Flap name), 双反四连杆, 链条连杆臂, 级联升降, 剪叉升降, 投石器, 支撑面积 (footprint), 手动控制 / 自动, 坦克模式 / 街机模式, 开关控制. EDP/COMP: 操作手 (driver), 维修区 (pit), 队号牌, 团队协作挑战赛, 联盟队友, 评委.
- Teacher review still needed (all `draft`): especially the Chinese not taken from an official source — BLD: 孔距 (pitch), 智能端口, 凸轮, 凸轮从动件, 齿数, 接口; CODE: block-type names (堆叠积木, 帽子积木, C形积木, 报告积木) and the six `concepts` terms. Also level assignments.
- Unverified fact claims in drafts: "continuous racks can be joined end to end" (BLD-075); IQ and V5 share the same square shaft size (SKU 276-1149 listed for `shaft`).

## 12. Working notes (handoff for the next session)

**Where things are**
- Local repo: `~/Projects/vex-iq-vocab` → GitHub `insufficientdoubt/vex-iq-vocab` (public), branch `main`, GitHub Pages from `main` root.
- Every push runs `validate.py` (GitHub Action) and rebuilds Pages (1–2 min). The app re-checks `vocab.csv` on every load and versions image URLs, so updates show without cache problems (users may need one hard refresh after app changes).
- Run the app locally: `python3 -m http.server 8000` in the repo, open `http://localhost:8000/app/`.

**How rows were added** (so new domains follow the same pattern)
- Seed a domain with a one-off Python script that builds rows (IDs assigned in order, `confused_with` written as term names and resolved to IDs, cross-domain refs as raw IDs like `BLD-001`), then appends to `data/vocab.csv` with `csv.DictWriter(..., lineterminator="\n")`. Keep column order from the CSV header. Run `python3 validate.py` after every change; it catches >75-char definitions, bad IDs, missing images, unknown SKUs, stray spaces.
- Small additions: append one row the same way; next ID = last ID in that domain + 1. Never renumber.
- Columns are in this order: id, term_en, aka, zh, short_def, explanation, example, confused_with, blocks, python, domain, subdomain, tags, level, season, image, ref_url, stem_lab, store_skus, status.

**Images**
- Square PNG, white background, 600×600, quantized to keep ≤ ~200 KB. `python3 tools/contact_sheet.py <DOMAIN>` → `build/contact-sheet-<DOMAIN>.png` (build/ is git-ignored) to eyeball them.
- Concept drawings: add a function to `tools/diagrams.py` and an entry in `DIAGRAMS` (keyed by `term_en`), then `python3 tools/diagrams.py` (redraws all). CODE drawings are auto-cropped/centered by `fit()`. Use shapes, not ✓/✗ glyphs (Arial lacks them).
- Kit-part drawings were cropped from the poster PDF rendered at 300 dpi (vector art, no embedded images): find the label with `pdftotext -bbox-layout`, take the nearest non-white blob; small/crowded parts needed manual boxes.
- VEX Library screenshots: article images are at `https://kb.vex.com/hc/article_attachments/<id>` and download fine with curl; find them via the Help Center API (article `body` HTML lists `<img src alt>`).
- Credit every non-original image in `images/CREDITS.md`.

**Fetching from VEX sites (gotchas)**
- vexrobotics.com, vexstore.cn, api.vex.com and kb.vex.com sit behind Cloudflare: curl/WebFetch get 403. Use the in-app browser and run `fetch()` from a page on the same site. If a "verify you are human" checkbox appears, don't click it — ask the user. (The store sometimes passes on its own after a few seconds.)
- vexstore.cn: on the IQ listing page, `window.algoliaConfig` gives the public search key; query `<indexName>_products` with `filters=vex_classroom:IQ`, `hitsPerPage=1000`. Product image URLs: strip the `/cache/<hash>/` part for full size. Images download fine with curl.
- api.vex.com: HTML pages are blocked even to in-page fetch; use `/iq2/searchindex.js` (titles + anchors, to verify `ref_url` anchors) and `/iq2/_sources/home/<page>.md.txt` (block text in ```` ```{code-block} scratchblock ```` fences, Python usage lines).
- VEXcode Chinese: on api.vex.com, load `/assets/scratchblocks/translations-all.js` with a fake `scratchblocks.loadLanguages` to capture the language objects; use `zh_cn.commands` (`iq2*`, `common*`, `brakeType*`, …), `zh_cn.dropdowns`, `zh_cn.palette`.
- `git push` occasionally fails with an SSL error from China; just retry.

**Next steps**
1. EDP and COMP: holistic review and fill-in from other sources (game manual, RECF judging, notebook rubric). SEASON (current game; `season` column required).
2. Sentence frames (`data/frames.csv`), including respectful referee questions and judge-interview frames.
3. Generators: Kahoot import, flashcards, handouts (reference = with Chinese, review = without).
