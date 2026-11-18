# UI/UX Craft Pro (`ui-ux-pro-max`)

A unified, single-source design and frontend engineering skill for AI coding agents — synthesizing structural taste, optical mathematics, surface-aware routing, React/Next.js performance engineering, interactive stage archetypes, asymmetric spring physics, and a deterministic `--strict` audit gate in one lightweight repository (`~2.3 MB`).

Built upon [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) and strengthened by unifying proven methodologies from five flagship agent skill systems (`pbakaus/impeccable`, `Leonxlnx/taste-skill`, `arham777/ui-ux-kit`, `vercel-labs/agent-skills`, and `Light0305/Light-UI-UX`).

---

## Unified 6-in-1 Skill Synthesis

Instead of forcing developers to wire up six conflicting, multi-megabyte repositories with overlapping Node binaries or 50+ MB databases, `ui-ux-craft-pro` fuses their strongest engineering mechanisms into a single clean workflow:

| Integrated Source | What We Adopted & Upgraded |
|---|---|
| **`nextlevelbuilder/ui-ux-pro-max-skill`** | Zero-network BM25 search engine (`search.py`) + expanded **12 Interactive Stage Archetypes** (`data/stage-archetypes.csv`) — stripped of duplicate platform mirrors (`.claude/`, `skills/`, `cli/`, `src/`, `stack/`). |
| **`pbakaus/impeccable`** | **4 Visitor Modes** (`Persuade / Operate / Read / Experience`), **Design Steering Verbs** (`polish`, `bolder`, `quieter`, `distill`, `harden`, `critique`), **Cognitive Load** ($\le 4$ choices rule) + **Nielsen 10-Heuristic** rubric, and browser surface theming (`::selection`, `caret-color`, scrollbars). |
| **`Leonxlnx/taste-skill`** | **6 Business/Trade Kinds** keeping effects/shaders strictly on tech/gaming/hardware surfaces while enforcing real photography on physical venues, `100svh` height containment at `700–800px`, plain 50/50 split hero rejection, and phantom horizontal-scrollbar fixes. |
| **`arham777/ui-ux-kit`** | **Category-Reflex Test**, **1-Sentence Falsifiable Concept**, **OKLCH Derived Dark Mode** & **3-Move Typography** (`Personality → Category → Face`), plus **Two-Round Non-Destructive Redesign** and collision-aware popovers. |
| **`Light0305/Light-UI-UX`** | **Vague Prompt → Physical CSS Translator**, **4 Stale Visual Clusters Denylist**, **19 Zero-Tolerance Bans** (no eyebrows/kickers, no nested cards, no 3px side stripes), **Hard Page Budgets** (Chanel's Rule), and **Dual-Track Latin vs. CJK Typography Law**. |
| **`vercel-labs/agent-skills`** | **8 Priority Tiers of React/Next.js Performance** (waterfall elimination, barrel bans, Server Action auth, render-time derivation, `useRef` tick isolation), **Compound Component Composition**, **React 19** `ref`-as-prop/`use()`, and **9 CWV Levers** (`vercel-react-and-web-engineering.md`). |

---

## Why `ui-ux-craft-pro` vs Standalone Upstream Skills

- **Deterministic Python `--strict` CLI Gate (`scripts/audit_anti_slop.py`):** Goes beyond prompt suggestions to fail CI/builds on AI purple/indigo gradients, hype copy/personas (`SaaSify`, `Alex Chen`, `10x faster`, `Streamline Your Workflow`, `Welcome back, Alex`), `SURFACE_SLOP` thick colored side stripes or neon glow halos, `PHANTOM_SCROLLBAR` horizontal tracks, `SKIPPED_HEADING` jumps, positive `tabindex`, missing `tabular-nums`, dead static pages, React 19 `forwardRef` usage, and WCAG regressions.
- **Photorealistic Cutout Pipeline (`scripts/extract_studio_cutout.py`):** 4-Phase pipeline using `rembg` neural segmentation + `distance_transform_edt` RGB de-haloing + dual-tone `#ECECEA` / `#828891` contrast contact sheets + mandatory headless Chrome screenshot checks before delivery.

---

## Searchable Local Catalog (`data/`)

- **12** interactive stage archetypes (`stage-archetypes.csv`)
- **79** searchable visual styles (**50** active)
- **192** product palettes & UI reasoning profiles
- **74** curated font pairings & Google Font entries
- **119** UX & accessibility guidelines
- **105** icon rules & vector conventions
- **28** GSAP & Living UI choreography presets
- **25** chart types across **22** frontend/mobile/desktop stacks

---

## Quick Install (Works Across Modern AI Coding Tools)

Clone this repo and copy the single-source core (`SKILL.md`, `data/`, `references/`, `scripts/`) into your coding agent's skills directory:

| Agent / Tool | Target Directory |
|---|---|
| **Antigravity** | `~/.gemini/config/skills/ui-ux-pro-max/` |
| **Claude Code** | `~/.claude/skills/ui-ux-pro-max/` |
| **Cursor** | `.cursor/skills/ui-ux-pro-max/` or `~/.cursor/skills/ui-ux-pro-max/` |
| **Codex / Universal** | `~/.codex/skills/ui-ux-pro-max/` |

```powershell
git clone https://github.com/CaptainFatih61/ui-ux-craft-pro.git
$dst = "$env:USERPROFILE\.gemini\config\skills\ui-ux-pro-max"
New-Item -ItemType Directory -Force -Path $dst | Out-Null
Copy-Item SKILL.md, data, references, scripts -Destination $dst -Recurse -Force
```

---

## CLI Toolkit (`scripts/`)

1. **Generate a complete design system (with `--variance`, `--motion`, `--density` dials):**
   ```bash
   python scripts/search.py "fintech analytics dashboard" --design-system --variance 7 --motion 6 --density 8 -p "App"
   ```
2. **Search specific domains or stacks:**
   ```bash
   python scripts/search.py "fashion lookbook runway" --domain stage
   python scripts/search.py "keyboard focus modal" --domain ux
   python scripts/search.py "re-render list optimization" --stack nextjs
   ```
3. **Run the Strict Anti-Slop, Surface & Accessibility Audit:**
   ```bash
   python scripts/audit_anti_slop.py . --strict
   ```
4. **Extract clean neural studio cutouts (`rembg` + de-haloing + dual-tone contact sheet):**
   ```bash
   uv run --with pillow --with numpy --with opencv-python-headless --with rembg \
     --with onnxruntime --with scipy python scripts/extract_studio_cutout.py \
     input.png output.png --mode model --clean-leg-floor --contact-sheet check.png
   ```
5. **Validate all 36 runtime CSV tables:**
   ```bash
   python scripts/validate-csv.py
   ```

---

## Reference Manuals (`references/`)

- [`taste-and-surface-gates.md`](references/taste-and-surface-gates.md) — Dual-axis surface/trade routing, 19 zero-tolerance bans, stale cluster denylist, 3-move OKLCH/typography rules, snap carousel CSS & steering/heuristic rubrics
- [`vercel-react-and-web-engineering.md`](references/vercel-react-and-web-engineering.md) — 8 React/Next.js optimization tiers, compound component composition, React 19 APIs & Core Web Vitals levers
- [`craft-physics-and-optics.md`](references/craft-physics-and-optics.md) — Concentric corner radius math, specular glass bevels, 3-tier luminance ladder & neural cutout pipeline
- [`living-ui-choreography.md`](references/living-ui-choreography.md) — Blueprints 1–13 & spring physics presets
- [`quick-reference.md`](references/quick-reference.md) & [`pro-rules.md`](references/pro-rules.md) — 119 UX guidelines & mobile/native pre-delivery checklists

---

## Flagship Pure-Code Showcases (`projects/`)

- [`projects/cadra-dashboard/`](projects/cadra-dashboard/index.html) — Living telemetry workspace, 10×10 dot-matrix capacity grids & diagonal staggered KPI architecture
- [`projects/vertix-dashboard/`](projects/vertix-dashboard/index.html) — High-craft financial cockpit with clip-path pill navigation & frosted card controls

---

## Repository Structure

```text
├── SKILL.md         # Master workflow routing & 4-Pillar / 4-Phase engineering rules
├── data/            # 36 zero-network BM25 CSV tables (incl. stage-archetypes & motion)
├── references/      # Taste/surface gates, Vercel React engineering, optics, choreography & UX
├── scripts/         # search.py, audit_anti_slop.py, extract_studio_cutout.py, validate-csv.py
└── projects/        # Flagship zero-dependency HTML showcases passing --strict audit
```

## License

MIT — see [LICENSE](LICENSE). Built upon [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill).
