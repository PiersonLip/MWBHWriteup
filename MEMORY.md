# Project memory

Standalone browser explainer for arXiv:2610.07152 (Kiato, Lipschultz, Kalogera et al. — Galactic BHs with POSYDON).

## Deliverable

- Single self-contained file: `index.html` (HTML + CSS + canvas JS, no build step).
- Serve locally (e.g. `python3 -m http.server 8765`) and open `/` or `/#galaxy`.

## Content editing (Obsidian vault)

- Vault path: `vault/` (open that folder in Obsidian).
- Chapters: `vault/chapters/*.md`; hero/footer: `vault/00 Home.md`; how-to: `vault/00 Workflow.md`.
- `Glossary.md`: site tip blurbs; matching terms also have appended `### From layman writeup` drafts from `~/research/laymanPaperWriteup` (Roman, Gaia, natal kick, etc.) — does not auto-apply to HTML.
- Obsidian hotkeys/plugins/themes/snippets synced from `~/notes/obsidianNotes` (plugin `data.json` gitignored; `semantic-auto-linker` not committed — bundled API key).
- Tips syntax: `[term]{tip: definition goes here}`
- Nested tips: site builds a glossary from all `.tip[data-tip]` terms and linkifies matches inside open tip bubbles (hover MESA inside POSYDON).
- Figure blocks only sync **cap / title / hint** — do not add/remove `:::figure` blocks.
- Apply vault → site: `python3 scripts/apply_vault.py`
- Resync site → vault (overwrites `chapters/` + Home; re-export may wipe Glossary layman sections): `python3 scripts/export_to_vault.py`
- Shared logic: `scripts/content_lib.py`

## Paper concepts covered

- Natal kicks / Blaauw mass loss / bound vs disrupted binaries (kick orbit interactive).
  - Kick canvas timeline: pre ≈2.4s → **flash hold ≈1.2s** (kick arrow + `v_kick` label) → post; full cycle ≈8.8s.
- Channel demographics (~4e8 BHs; mostly isolated today).
- Wind-driven vs stable MT (~13 M☉ feature), CE efficiency.
- Galactic seeding (§II.3): POSYDON survivors → MW components → gala-style orbit integration → kick in Galactocentric frame → present-day catalog (Gaia/Roman hooks).

## Galaxy viz (`#galaxy`) — current behavior

- 3D canvas schematic: birth → pre-SN disk arc → SN+kick → separate BH (white) + companion (gold) trails.
- Examples (not a continuous kick slider): **Mild** / **Typical** / **Strong** (`GAL_EXAMPLES`).
- Physics notes:
  - Units: `KMS_MYR_TO_KPC = 0.001022712165` (km/s·Myr → kpc). Wrong (×1000) values blow up orbits.
  - Flat rotation curve in-plane (`Vc ≈ 220`); vertical `nu2 ≈ 0.005`.
  - Verlet integrator shared for pre/post paths.
- Camera: drag yaw/pitch (near face-on → nearly edge-on), scroll zoom ~0.72–1.55×.
- Fullscreen: **stage only** (`#gal-stage`), not the controls.
- Idle spin: only after **5s inactivity**, or **immediately when the story hits 100%**.
- Easter eggs: globulars ω Cen, M13, M22 (hover to label). Field stars ~1050 + cluster members.
- Shortcuts: `R` restart; `1`/`2`/`3` examples; `Space` play/pause **only while fullscreen**.

## Writing / UX conventions

- Casual copy, no em dashes.
- Hover glossary tips via `.tip[data-tip]`.
- Teaching-faithful schematics, not raw POSYDON dumps.

## Workflow (agent)

- When a chunk of work is clearly done: **commit** with a concise why-focused message, then **push** to `origin`.
- Keep this `MEMORY.md` updated when behavior, controls, physics constants, or scope change.
- Do not commit `verify/` screenshots or secrets.

## Repo

- GitHub remote via `gh`; default branch `main`.
- Primary artifact to review: `index.html`.
