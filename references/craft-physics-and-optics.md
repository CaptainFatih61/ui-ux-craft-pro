# High-Craft Optics & Living UI Physics Reference

This reference documents the mathematical and optical engineering standards for crafting elite, production-grade interfaces that surpass generic AI-generated aesthetics.

---

## 1. Concentric Corner Radius Mathematics

When nesting rounded containers (e.g. a card containing an image, badge, or button), the corner radii must maintain geometric concentricity. Reusing the same radius creates an optical illusion of pinching, distortion, and visual clumsiness.

### The Concentric Formula
$$\mathbf{R_{\text{outer}} = R_{\text{inner}} + \text{Padding}}$$
$$\mathbf{R_{\text{inner}} = \max\left(0, R_{\text{outer}} - \text{Padding}\right)}$$

### Common Scale Pairings (8px Grid Spacing)

| Outer Container Radius | Internal Padding | Inner Element Radius | Tailwind Token Pairing |
|---|---|---|---|
| `24px` (`rounded-3xl`) | `8px` (`p-2`) | `16px` (`rounded-2xl`) | Outer `rounded-3xl p-2` $\to$ Inner `rounded-2xl` |
| `24px` (`rounded-3xl`) | `12px` (`p-3`) | `12px` (`rounded-xl`) | Outer `rounded-3xl p-3` $\to$ Inner `rounded-xl` |
| `20px` (`rounded-[20px]`) | `8px` (`p-2`) | `12px` (`rounded-xl`) | Outer `rounded-[20px] p-2` $\to$ Inner `rounded-xl` |
| `16px` (`rounded-2xl`) | `8px` (`p-2`) | `8px` (`rounded-lg`) | Outer `rounded-2xl p-2` $\to$ Inner `rounded-lg` |
| `12px` (`rounded-xl`) | `4px` (`p-1`) | `8px` (`rounded-lg`) | Outer `rounded-xl p-1` $\to$ Inner `rounded-lg` |
| `12px` (`rounded-xl`) | `8px` (`p-2`) | `4px` (`rounded-md`) | Outer `rounded-xl p-2` $\to$ Inner `rounded-md` |

> **Anti-Pattern:** Stacking identical border radii (e.g., `<div class="rounded-2xl p-4"><img class="rounded-2xl" /></div>`). The corners will appear detached and deformed.

---

## 2. 1px Specular Hairlines & Glass Lensing

Flat translucent panels (`bg-white/10 backdrop-blur`) look muddy and unfinished without simulated edge lighting (specular reflection).

### The Dual-Edge Lighting Formula
Real glass exhibits light refraction at the top bevel and ambient shadow at the bottom edge.

```css
/* Light Mode Specular Hairline */
.glass-lensing-light {
  background: rgba(255, 255, 255, 0.75);
  backdrop-filter: blur(16px) saturate(180%);
  -webkit-backdrop-filter: blur(16px) saturate(180%);
  border: 1px solid rgba(255, 255, 255, 0.6);
  box-shadow: 
    inset 0 1px 1px 0 rgba(255, 255, 255, 0.9),  /* Top specular highlight */
    0 10px 30px -10px rgba(0, 0, 0, 0.06),         /* Ambient soft drop shadow */
    0 1px 2px 0 rgba(0, 0, 0, 0.04);              /* Grounding contact shadow */
}

/* Dark Mode Specular Hairline */
.glass-lensing-dark {
  background: rgba(28, 25, 23, 0.7);
  backdrop-filter: blur(20px) saturate(150%);
  -webkit-backdrop-filter: blur(20px) saturate(150%);
  border: 1px solid rgba(255, 255, 255, 0.08);
  box-shadow: 
    inset 0 1px 0 0 rgba(255, 255, 255, 0.15),   /* 1px Specular top bevel */
    0 20px 40px -15px rgba(0, 0, 0, 0.5);         /* Deep elevation shadow */
}
```

---

## 3. Surface Luminance Elevation Ladder

Never pick random hex codes for elevated layers (dialogs, tooltips, cards, canvas). Maintain consistent perceptual lighting steps:

### Light Mode Surface Hierarchy
- **Canvas / Root Background (`Surface 0`):** `#FAFAF9` (Stone-50) or `#F8FAFC` (Slate-50)
- **Primary Card Surface (`Surface 1`):** `#FFFFFF` (Pure white card with soft 1px border `#E7E5E4`)
- **Interactive Elevated Surface (`Surface 2`):** `#FFFFFF` with elevated shadow `0 12px 32px -8px rgba(0,0,0,0.08)`
- **Modal / Floating Drawer (`Surface 3`):** `#FFFFFF` with ambient scrim + dual hairline

### Dark Mode Surface Hierarchy
- **Canvas / Root Background (`Surface 0`):** `#0C0A09` (Stone-950) or `#09090B` (Zinc-950)
- **Base Card Surface (`Surface 1`):** `#1C1917` (Stone-900) + border `rgba(255,255,255,0.08)`
- **Elevated Hover / Flyout (`Surface 2`):** `#292524` (Stone-800) + top highlight `inset 0 1px 0 rgba(255,255,255,0.12)`
- **Modal / Floating Overlay (`Surface 3`):** `#322E2B` (Stone-750) + backdrop-blur scrim

---

## 4. Spring Physics & Asymmetric Motion

Linear motion and generic ease-in-out (`transition: all 0.3s ease`) feel robotic and sluggish. Elite interfaces use **asymmetric acceleration**: immediate explosive start with a long, damped deceleration.

### Standard Easing Tokens

| Intent | Timing / Easing | Recommended CSS / Token |
|---|---|---|
| **Modal / Drawer Reveal** | Fast in, smooth deceleration | `cubic-bezier(0.16, 1, 0.3, 1)` (duration: 380ms) |
| **Micro-Interactions (Hover/Press)** | Crisp, instant response | `cubic-bezier(0.2, 0.8, 0.2, 1)` (duration: 180ms) |
| **Drawer Dismissal / Exit** | Accelerating exit | `cubic-bezier(0.4, 0, 1, 1)` (duration: 220ms) |
| **Spring Damping Constants** | Physics Simulation | Stiffness: `320`, Damping: `28`, Mass: `1.0` |

---

## 5. Live Number Tickers & Tabular Data

Whenever an interface displays monetary amounts, counters, stock indicators, or dynamic telemetry:
1. **Always apply `font-variant-numeric: tabular-nums;`** (Tailwind: `tabular-nums`).
2. This locks the character bounding box so fluctuating numbers do not cause horizontal layout jitter or vibrating prices.
3. For animated counters, roll the decimal values vertically or update inner text seamlessly without reflowing adjacent words.

---

## 6. Dynamic Card Spotlight Shader Effect

Simulates a directional flashlight moving across luxury products or tech cards:

```javascript
// Attaches a radial gradient highlight to the mouse coordinates
document.querySelectorAll('.spotlight-card').forEach(card => {
  card.addEventListener('mousemove', (e) => {
    const rect = card.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    card.style.setProperty('--mouse-x', `${x}px`);
    card.style.setProperty('--mouse-y', `${y}px`);
  });
});
```

```css
.spotlight-card {
  position: relative;
  overflow: hidden;
}
.spotlight-card::before {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(
    600px circle at var(--mouse-x, 0) var(--mouse-y, 0),
    rgba(255, 255, 255, 0.08),
    transparent 40%
  );
  pointer-events: none;
  opacity: 0;
  transition: opacity 300ms ease;
}
.spotlight-card:hover::before {
  opacity: 1;
}
```

---

## 7. Neural Cutout & De-Haloing Pipeline (Physical & Apparel Stages)

Naive RGB color-keying or PowerShell border flood-fills fail on real human subjects, studio cyclorama gradients, white fabrics (puncturing chests/tees), and dark denim rims (leaving 1–2px light-grey rectangular artifacts or white fringes). Whenever physical subjects, apparel, or studio footwear must be composited seamlessly onto CSS stages:

1. **Neural Alpha Fusion (`rembg`)**:
   - Full-body studio subjects use `u2net_human_seg` + `isnet-general-use` weighted fusion with lower-leg neutral floor gap suppression (`scripts/extract_studio_cutout.py --mode model --clean-leg-floor`).
   - Bright white tops paired with dark denim use `isnet-general-use` for razor-sharp lower contours, `u2net` near shoe soles (`y >= 89%`), and eroded denim boundaries (`3x3` ellipse) (`--mode white-garment`).
   - Studio flat-lays and sneakers use `isnet-general-use` (or `u2net --symmetrize-x` for low-contrast garments and border-cleared morphological closing `--fill-holes` for white sneaker uppers).
2. **RGB Edge Decontamination (`distance_transform_edt`)**:
   - Before upscaling or compositing, erode the solid core mask (`alpha >= 235`, `3x3`–`5x5` ellipse) and map every semi-transparent fringe pixel (`alpha < 248`) toward the nearest interior foreground RGB color via `scipy.ndimage.distance_transform_edt`. This eliminates studio wall bleed without shrinking silhouette softness.
3. **Interior-Only Sharpening**:
   - When enhancing upscaled video or studio crops with an unsharp mask (`cv2.addWeighted`), apply sharpened RGB **only** inside `cv2.erode(alpha >= 248, (5, 5))` so boundary anti-aliasing never develops a 1px white overshoot ring.
4. **Dual-Tone Contact-Sheet Gate**:
   - Inspect every extracted cutout composited across both studio base (`#ECECEA`) and mid-slate contrast (`#828891`) bands via `--contact-sheet` before writing HTML.
   - Standard CLI invocation:
     ```bash
     uv run --with pillow --with numpy --with opencv-python-headless --with rembg \
       --with onnxruntime --with scipy python scripts/extract_studio_cutout.py \
       input.png output.png --mode model --clean-leg-floor --contact-sheet sheet.png
     ```
