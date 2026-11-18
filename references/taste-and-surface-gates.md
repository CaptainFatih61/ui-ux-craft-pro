# Taste, Surface Routing & Anti-AI-Slop Engineering Gates

Unified field manual synthesizing architectural rules from **Impeccable**, **Taste-Skill**, **UI/UX Kit**, and **Light-UI-UX** into concrete, verifiable interface engineering gates.

---

## 1. Dual-Axis Surface & Trade Router

Classify every brief along two orthogonal axes **before writing CSS or markup**:

### Axis A: 4 Visitor Modes (World-Building Boundary)

| Visitor Mode | Typical Surfaces | Layout & Creative Authority | Required First-Viewport Contract |
|---|---|---|---|
| **1. `Persuade`** | Landing pages, launches, marketing, pricing | **Visual world owns the composition.** Must pass the **Peer Replacement Test** (anchor the hero in an unmistakable domain artifact/ritual). | Primary `Verb + Object` CTA above the fold at `700–800px` laptop heights; $\ge 1$ scroll-driven (`scrub`) or choreographed narrative moment. |
| **2. `Operate`** | SaaS workbenches, dashboards, admins, editors, settings | **World lends ONLY 4 traits: Font, Palette, Density, `1` micro-detail.** Never apply playful costumes or marketing banners inside tools. | Zero welcome slogans (`"Welcome back!"`); compact `28–34px` toolbar; $10\text{--}20+$ operable items immediately visible. Pick layout by **Primary Verb** (`Queue`, `Table`, `Canvas`, `Timeline`, `Map`, `Board`, `Actionable Monitor`, `Chat+Artifact`, `Index Gallery`). |
| **3. `Read`** | Docs, blogs, articles, changelogs, reports | **Outer chrome holds brand framing; reading column stays dead quiet.** Zero background texture or distracting motion under prose. | Measure `60–75ch` (Latin) / `25–40` chars (CJK); clear sequential `<h1> → <h2> → <h3>` outline; code blocks & callouts cleanly offset. |
| **4. `Experience`** | Portfolios, galleries, lookbooks, interactive product stages | **The artifact leads from pixel 0; UI chrome recedes.** | Zero boxed clutter blocking the hero canvas; direct pointer/drag/physics feedback (`--domain stage`). |

### Axis B: 6 Business / Trade Kinds (`software | gaming | tech | product | service | place`)

- **Tech Surfaces (`software`, `gaming`, `tech` hardware):** May use **at most 1 focal effect** (CSS atmospheric ground, shader/WebGL2 stage, or kinetic choreography) and live interactive product slices (`app-frame` / diff / live telemetry). Hardware relies on crisp studio photography or user-requested 3D renders — never fake `<svg>` mockups.
- **Physical & Local Surfaces (`product`, `service`, `place`):**
  - Cafes, bakeries, hotels, studios, clinics, furniture, apparel, food **must NOT use dark-neon sci-fi effects, shader grounds, particle confetti, or technical monospace costumes**.
  - Lead with **real studio/on-location photography**, flat tactile color tokens, strong display typography, and photo/type editorial moments (`scripts/extract_studio_cutout.py` + `--contact-sheet` for transparent apparel/product cutouts).
  - Never invent real phone numbers, house street numbers, postcodes, VAT numbers, or coordinates on fictional demos (`street/district` + `.example` addresses only).

### Vague Prompt → Concrete CSS/Optical Translation Table

| Prompt Adjective | Concrete Physical & Optical Translation |
|---|---|
| **"Premium / High-Craft"** | Inset canvas hierarchy (`Surface 0 → 1 → 2`) + concentric radii ($R_{\text{outer}} = R_{\text{inner}} + \text{Padding}$) + `1px` specular bevels + hue-tinted dual-layer elevation shadows + $\ge 4{:}1$ display-to-body scale + themed `::selection`, `caret-color`, and scrollbar. |
| **"Tech / Futuristic / AI"** | Reject cliché indigo/violet glow and sparkles! Use deep obsidian (`#08090a`) or archival silver (`#f2f2f0`) + exposed `1px` grid hairlines + `JetBrains Mono` (`tabular-nums`) telemetry + interactive slice (`app-frame` or `1` shader stage). |
| **"Minimal / Clean"** | $\le 3$ colors total, $\le 5$ type sizes, zero card borders — let `80–160px` vertical rhythm, `2–3` shared left alignment axes, and strong scale contrast structure the screen. |
| **"Editorial / Warm"** | Reject stale `#F5EFE6 + terracotta + italic Fraunces` cliché! Pull saturated tactile pigments from real materials (buckram cloth, archival cobalt, crisp newsprint `#F4F4F0` + `#060606`) paired with editorial serif contrast and asymmetric columns. |
| **"Fluid / Playful"** | Asymmetric spring deceleration (`cubic-bezier(0.16, 1, 0.3, 1)`), immediate `scale(0.97)` tactile press, shared-element `clip-path` pill indicator (`0.36s` lead / `0.55s` trail), and interactive stage containers rather than uniform card grids. |

---

## 2. Concept Commitment, Color Strategy & Typography Laws

### Mandatory Pre-Build Concept & Anti-Reflex Checks
1. **Category-Reflex Test:** If a stranger can guess your palette solely from the industry (*fintech -> navy+gold*, *healthcare -> teal+white*, *crypto -> neon-on-dark*, *AI -> purple-indigo gradient*), rework until the choice is intentional and non-generic (unless mandated verbatim by the brief).
2. **Falsifiable 1-Sentence Concept:** Write upfront: *"Concept: `<concrete organizing metaphor>` expressed across `<layout>`, `<type>`, `<color>`, and `<motion>`."* Must appear in $\ge 3$ axes.

### 4 Stale AI Visual Clusters (Ban List)
1. Warm cream `#F5EFE6` + terracotta `#D97757` + italic `Fraunces`/`Playfair`.
2. Near-black + acid green/cyan matrix + all-caps mono subtitles everywhere.
3. Fake yellowed vintage newspaper (`ISSUE NO. 04 · EST. 2026`) plastered on modern software.
4. Soft pastel mesh backdrop + white `rounded-2xl` cards + 4 round stat tiles (`100%`, `10x`, `24/7`, `99.9%`). Use realistic domain metrics (`1,238`, `+1.83%`, `42ms`) in `tabular-nums`.

### Color Strategy in OKLCH
- Pick one strategy explicitly: **Restrained** (tinted neutrals + $\le 10\%$ accent — dashboard/product default), **Committed** (one dominant saturated hue), **Full Palette** (3–4 named roles), or **Drenched** (saturated field carries canvas).
- Tint neutral grays slightly toward brand hue (`chroma ~0.005–0.01`) instead of raw uncalibrated `#000`/`#fff` unless true OLED/brutalist ink is intended.
- **Dark mode is derived, not inverted:** elevate layers by increasing lightness (`#0C0A09 → #1C1917 → #292524`), soften drop shadows (depth comes from surface luminance + top `inset 0 1px` bevel), soften extreme accent chroma, and recompute WCAG AA contrast independently ($\ge 4.5{:}1$ body, $\ge 3.0{:}1$ large display/UI, `OKLCH ΔL >= 45` fast pre-check; never gray-saturation `<0.08` text over saturated color).

### 3-Move Typography System & Dual-Track Law

| Brand Personality | Category | Display / Heading Options | Body Pairing |
|---|---|---|---|
| **Corporate / SaaS** | Grotesque sans | Geist, Hanken Grotesk, Mona Sans, Plus Jakarta Sans | Same family, weight contrast |
| **Editorial / Luxury** | High-contrast serif | Fraunces, Bodoni Moda, Instrument Serif, Cormorant | Clean grotesque sans |
| **Warm / Human** | Humanist sans / soft | Epilogue, Bricolage Grotesque, Schibsted Grotesk | Mulish, Nunito Sans |
| **Bold / Athletic** | Condensed / wide display | Anton, Archivo Expanded, Clash Display | Neutral grotesque |
| **Playful / Consumer** | Rounded / expressive | Fredoka, Baloo 2, Bagel Fat One | Nunito, Rubik |
| **Technical / Dev** | Mono + neo-grotesque | JetBrains Mono, IBM Plex Mono | IBM Plex Sans, Inter (UI body only) |

- **Latin vs CJK Dual-Track Law:** Latin display H1 uses `line-height: 0.95–1.10`, tracking `-0.02em` to `-0.04em`. CJK display H1 MUST use `line-height: 1.25–1.40` (never `<1.20`) and tracking `0` to `0.02em` (never negative tracking on CJK!). Body measure: `45–75ch` Latin / `25–40` CJK chars.
- **Never repeat a stat/metric string identically across card heading, slider readout, and footer caption** (*Number-Deduplication Law*), and **never draw both a read-only progress bar and an interactive slider** (*Single-Ruler Law* — merge into one interactive control).

---

## 3. The 19 Zero-Tolerance Bans & Hard Subtraction Budgets

If $\ge 3$ bans appear without an explicit brief instruction, refactor before delivery:

1. **No kicker / eyebrow mini-labels** (uppercase `FEATURES` or pill+dot tags) stacked above H1/H2 headings unless strict structured metadata demands it.
2. **No card-inside-card nesting** (use whitespace, `1px` hairlines, or contrast wells instead of inner bordered boxes).
3. **No 3-equal icon+heading+blurb card grids** placed directly under the hero.
4. **No colored thick side/top accent stripes** (`border-left: 3px+ solid` or `border-t-4` on rounded cards/alerts).
5. **No unrequested `background-clip: text` rainbow/purple gradient headings**.
6. **No AI purple/indigo defaults (`#6366f1`, `#8b5cf6`, `#667eea`) or zero-offset colored neon halos**.
7. **No emojis (`🚀 ✨ 💡`) used as structural UI icons** — use consistent monochrome SVG libraries (`Phosphor`, `Heroicons`, `Radix`, `Tabler`).
8. **No decorative `01 / 02 / 03` sequence numbers** on non-sequential unordered blocks.
9. **No fake browser traffic lights** or `9:41` status bars unless intentionally building an OS window simulator.
10. **No fake static sparklines or `+12.4%` numbers** detached from interactive data/context.
11. **No decorative pulsing dots (`animate-ping`)** on static badges/marketing pills.
12. **No cheap CSS/SVG shape-assembled illustrations** faking complex objects/characters — use real photography or studio cutouts.
13. **No polygon/circle CSS mask hacks** on photographic subjects — use true alpha PNG mattes (`scripts/extract_studio_cutout.py`).
14. **No burying photography under `> 90%` opaque scrims** (scrim only behind text zones).
15. **No prompt meta-leakage on screen** (`"Hero Section"`, `"Placeholder"`, `"Bento Grid"`, `"Lorem ipsum"`).
16. **No hollow AI buzzwords / fake personas** (`"10x faster"`, `"Streamline your workflow"`, `"Like never before"`, `"Unleash the power"`, `"Revolutionize your"`, `"SaaSify"`, `"Alex Chen"`).
17. **No welcome banners inside `Operate` workbenches**.
18. **No theatrical knob/CLI costumes** replacing standard fast controls in productivity UI.
19. **No apologetic/explanatory captions under photos** — let imagery carry itself.

### Hard Subtraction Ceilings & Browser Chrome Polishing
- **Budgets:** $\le 2$ font families ($\le 3$ w/ mono), `4–6` distinct size steps, `2–3` weights, $\le 10\%$ accent area (Restrained), $\le 4$ semantic color roles, $\le 3$ cards/row, $\le 3$ data points/card, $\ge 25\%$ viewport whitespace, max `1` heavy signature ornament per page.
- **Copy Necessity Check:** If deleting a subtitle, helper text, or tag leaves the decision equally clear, delete it (keep required labels, error guidance, units, and billing terms).
- **Theme Browser Surfaces (`impeccable` reflex check):** Customize `::selection`, `caret-color`, custom scrollbars (`scrollbar-width: thin`), `text-underline-offset`, `:focus-visible`, and `tabular-nums` from your palette tokens.

---

## 4. Surface Engineering Recipes

### Hero & Vertical Containment (`Persuade`)
- Wrap above-the-fold heroes in `min-h-svh` (`100svh`, never hardcoded `100vh`) and verify in headless Chrome across desktop widths **and** tight laptop heights (`700–800px`) with zero CTA clipping.
- **A plain 50/50 text-left / rounded-card-right split hero is a default fail** unless paired with a clear asymmetric spatial move (bleed-off edge, overlapping stage depth, or live working UI slice). Prefer centered editorial, oversized typography, full-bleed atmospheric composition, or asymmetric off-grid layouts.

### Zero-Scrollbar Horizontal Snap Carousel
Prevent both OS scrollbars and phantom cross-axis vertical bars (`overflow-x: auto` triggers `overflow-y: auto` unless overridden):
```css
.rail-track {
  display: grid;
  grid-auto-flow: column;
  overflow-x: auto;
  overflow-y: hidden;
  scroll-snap-type: x mandatory;
  scrollbar-width: none;
  -webkit-mask-image: linear-gradient(to right, transparent, #000 32px, #000 calc(100% - 32px), transparent);
}
.rail-track::-webkit-scrollbar { display: none; }
.rail-card { scroll-snap-align: start; }
```
Provide $\ge 44\times 44\text{px}$ Prev/Next keyboard controls (`role="region"` + `aria-label`) that switch to `behavior: "auto"` under `prefers-reduced-motion`.

### Dashboards, Tables & Floating Controls (`Operate`)
- Virtualize lists $\ge 50$ rows; right-align numerals with `tabular-nums`, left-align strings; include `aria-sort` and `empty / loading / error` states for every table and chart.
- Charts: Pie/donut $\le 5$ slices (else bar); never encode series solely via color (add pattern/direct labels; avoid red/green pairs); keep data marks $\ge 3{:}1$ and labels $\ge 4.5{:}1$.
- Floating UI (tooltips, popovers, selects, menus) must use collision-aware positioning (Native Popover API / CSS Anchor Positioning / Floating UI) so edges never clip at viewport bounds.

---

## 5. Design Steering Verbs & Cognitive Load Critique Rubric

Use focused verbs when refining an existing UI:
- **`polish`** — Fix alignment, optical padding, `:focus-visible`, states, and surface contrast without changing visual direction.
- **`bolder`** / **`quieter`** — Dial typographic contrast/visual tension up (`Persuade/Experience`) or dial excess ornament down (`Operate/Read`).
- **`distill`** — Strip redundant eyebrow tags, nested borders, and dead copy until core affordances breathe.
- **`harden`** — Add empty/loading/error states, narrow-viewport checks (`390px`), keyboard navigation, i18n text expansion, and boundary testing.
- **Two-Round Non-Destructive Redesign (`Diagnose → Refactor`):** First audit incumbent tokens, hierarchy defects, and broken states cleanly (`[Direct Fixes]` vs `[Upgrade / Reshape]`); only alter design tokens from the root out after scope is clear.

### Working Memory & Heuristic Review (`impeccable` Rubric)
- **Cowan's Working Memory Rule:** Limit simultaneous visible choices at any single decision point to **$\le 4$ items** (action buttons, sibling tabs, top nav links $\le 5$). Group secondary items progressively.
- **8 Cognitive Load Checks:** Single Focus · Chunking ($\le 4$/group) · Proximity Grouping · Visual Hierarchy · Sequential Decisions · Minimal Options · Zero Cross-Screen Memory Bridges · Progressive Disclosure.
- **Nielsen's 10 Usability Heuristics (Score 0–4 before final sign-off):** System Status · Real-World Language · User Control/Undo · Consistency · Error Prevention · Recognition over Recall · Accelerator Efficiency · Minimalism · Actionable Error Recovery · Contextual Help.
