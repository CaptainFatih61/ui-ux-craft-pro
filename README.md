# UI/UX Craft Pro (`ui-ux-pro-max`)

A high-craft design intelligence skill built for AI coding assistants to turn standard web, SaaS, dashboard, e-commerce, and app interfaces into crisp, tactile, production-grade UI — without generic AI slop.

## Philosophy & Scope

- **Core Focus (Standard UI Engineering)**: Enforces 3-tier surface elevation (`Surface 0 → 1 → 2`), concentric border-radius math ($R_{\text{outer}} = R_{\text{inner}} + \text{Padding}$), `1px` specular hairlines, `tabular-nums` metric stability, and asymmetric spring motion (`cubic-bezier(0.16, 1, 0.3, 1)`).
- **4-Phase Pipeline for Physical Stages**: When bespoke product, culinary, fashion, or lookbook stages are requested, separates **Source Acquisition → Neural Cutout & Dual-Tone Contact-Sheet Gate → 1:1 State UI Engineering → Headless Browser Screenshot & Audit Gate** instead of faking complex photography with primitive vector shapes or naive color-keying.

## Searchable Local Catalog

- **12** interactive stage archetypes (`data/stage-archetypes.csv`)
- **79** searchable visual styles (**50** active)
- **192** product palettes & UI reasoning profiles
- **74** curated font pairings & Google Font entries
- **119** UX & accessibility guidelines
- **105** icon rules & vector conventions
- **28** GSAP & Living UI choreography presets
- **25** chart types across **22** frontend/mobile/desktop stacks

## Quick Install (Single-Source Skill)

Clone or download this repository and copy its core skill files (`SKILL.md`, `data/`, `references/`, `scripts/`) into your AI tool's skills folder:

| Agent / Tool | Target Skill Directory |
|---|---|
| **Antigravity** | `~/.gemini/config/skills/ui-ux-pro-max/` |
| **Claude Code** | `~/.claude/skills/ui-ux-pro-max/` |
| **Cursor** | `.cursor/skills/ui-ux-pro-max/` (project) or `~/.cursor/skills/ui-ux-pro-max/` |
| **Codex / Universal Agents** | `~/.codex/skills/ui-ux-pro-max/` |

Example (PowerShell):

```powershell
git clone https://github.com/Qionzy/ui-ux-craft-pro.git
$dst = "$env:USERPROFILE\.gemini\config\skills\ui-ux-pro-max"
New-Item -ItemType Directory -Force -Path $dst | Out-Null
Copy-Item SKILL.md, data, references, scripts -Destination $dst -Recurse -Force
```

## CLI Tools (`scripts/`)

1. **Generate a full design system**:
   ```bash
   python scripts/search.py "fintech analytics dashboard" --design-system --variance 7 --motion 6 --density 8 -p "App"
   ```
2. **Query a specific domain or stack**:
   ```bash
   python scripts/search.py "fashion lookbook runway" --domain stage
   python scripts/search.py "keyboard focus modal" --domain ux
   python scripts/search.py "re-render list optimization" --stack nextjs
   ```
3. **Run the zero-dependency Anti-Slop & Accessibility Audit**:
   ```bash
   python scripts/audit_anti_slop.py . --strict
   ```
4. **Extract neural studio cutouts (`rembg` + `distance_transform_edt` de-haloing + contrast contact sheet)**:
   ```bash
   uv run --with pillow --with numpy --with opencv-python-headless --with rembg \
     --with onnxruntime --with scipy python scripts/extract_studio_cutout.py \
     input.png output.png --mode model --clean-leg-floor --contact-sheet check.png
   ```
5. **Validate CSV datasets**:
   ```bash
   python scripts/validate-csv.py
   ```

## Included Pure-Code UI Demos (`projects/`)

Lightweight, self-contained HTML/CSS/JS showcase interfaces audited with zero violations or warnings:

- `projects/cadra-dashboard/` — Telemetry workspace & split-pillar UI
- `projects/vertix-dashboard/` — Dense operational analytics dashboard
- `projects/luxury-ecommerce/` — Editorial boutique & drawer checkout
- `projects/healthcare-dashboard/` — Clinical patient & scheduling interface
- `projects/portfolio-dark/` — Dark editorial studio showcase
- `projects/saas-landing/` — Modern B2B SaaS landing architecture

## Repository Structure

```text
├── SKILL.md         # Master skill instructions & 4-Pillar workflow
├── data/            # 36 runtime CSV design/stack/stage tables
├── references/      # Craft physics, optics, living choreography & UX checklists
├── scripts/         # Search engine, anti-slop auditor, CSV validator & cutout CLI
└── projects/        # Self-contained pure-HTML showcase demos
```

## License

MIT — see [LICENSE](LICENSE). Built upon the open-source UI/UX Pro Max skill ecosystem.
