# Living UI & Choreography Engineering Blueprints

This reference equips AI agents to build **living, multi-state, choreographed interfaces** (Awwwards, Dribbble, and interactive product showcase caliber) rather than static, lifeless HTML documents.

---

## 0. The Stateful Living UI Mandate

When building any web application, dashboard, e-commerce store, fintech platform, or interactive landing page, **never deliver a dead static document**. Apply these 5 core laws:

1. **Stateful View Switching:** Navigation tabs (`Dashboard`, `Inventory`, `Analytics` or `Overview`, `Manage`, `Savings`) must dynamically switch views in-page using choreographed transitions (such as **Skeleton-to-Stagger** or **FLIP morphs**) rather than dead `href="#"` links.
2. **Physics-Driven Active Indicators:** Never use instant jumps or linear `transition: all 0.3s` for active tabs. Use **Asymmetric Lead/Trail Clip-Path Pills (`slidePill`)** or **Sliding Rim-Light Spotlights**.
3. **Morphing Micro-Chrome:** Search triggers, filter bars, and action pills should morph their bounds smoothly (e.g., a `40px` search icon button expanding into a `260px` input with a `⌘K` badge).
4. **Spatial & Tactile Object Presentation:** Products and hero objects must feel physical—use **Interactive Pendulum/Inertia Stages** with live color/material swatch crossfading, or **Exposed 1px Hairline Editorial Grids** with dual-image hover swaps (packshot $\to$ model/lifestyle shot).
5. **Living Telemetry Widgets:** Never render placeholder boxes for charts or stats. Render functional **10×10 Dot-Matrix Capacity Grids**, **Interactive SVG Spline Area Charts with Hover Scrubbers**, **Animated Arc Gauges**, and **Tactile Card Controls** (freeze toggles, PIN blur reveals, live range sliders with `tabular-nums`).

---

## Blueprint 1: Asymmetric Lead/Trail Clip-Path Pill (`slidePill`)

Instead of moving a background `<div>` behind tabs (which causes contrast glitches before the pill arrives), render a **duplicate full-size overlay layer** with inverted colors (`bg-stone-950 text-white` or `bg-white text-stone-950`) and clip it to the active tab using `clip-path: inset(top right bottom left round 999px)`.

**The Physics Secret:** When moving to a new tab, the **leading edge** travels faster (`0.36s`, `power3.out`) and the **trailing edge** follows (`0.55s`, `power3.inOut`), creating an organic liquid stretch-and-snap effect.

```javascript
/**
 * Asymmetric Elastic Clip-Path Pill Engine
 * @param {HTMLElement} pillOverlay - The full-size duplicate nav layer with inverted colors
 * @param {HTMLElement} navContainer - The parent navigation bar container
 * @param {HTMLElement} targetTab - The clicked/active tab button element
 * @param {boolean} animate - False on initial mount/resize, true on user click
 */
const pillState = { l: 0, t: 0, r: 0, b: 0 };

function slidePill(pillOverlay, navContainer, targetTab, animate = true) {
  const w = navContainer.scrollWidth;
  const h = navContainer.scrollHeight;
  const to = {
    l: targetTab.offsetLeft,
    t: targetTab.offsetTop,
    r: w - (targetTab.offsetLeft + targetTab.offsetWidth),
    b: h - (targetTab.offsetTop + targetTab.offsetHeight),
  };

  const clip = (e) =>
    `inset(${e.t}px ${e.r}px ${e.b}px ${e.l}px round 999px)`;

  if (!animate || window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    Object.assign(pillState, to);
    pillOverlay.style.clipPath = clip(pillState);
    return;
  }

  // Determine direction: moving right means 'r' is the leading edge; moving left means 'l' is the leading edge
  const movingRight = to.l > pillState.l;
  const [lead, trail] = movingRight ? ['r', 'l'] : ['l', 'r'];

  const draw = () => {
    pillOverlay.style.clipPath = clip(pillState);
  };

  if (window.gsap) {
    // Leading edge accelerates immediately
    gsap.to(pillState, {
      [lead]: to[lead],
      t: to.t,
      b: to.b,
      duration: 0.36,
      ease: 'power3.out',
      onUpdate: draw,
    });
    // Trailing edge follows with elastic lag
    gsap.to(pillState, {
      [trail]: to[trail],
      duration: 0.55,
      ease: 'power3.inOut',
      onUpdate: draw,
    });
  } else {
    Object.assign(pillState, to);
    draw();
  }
}
```

---

## Blueprint 2: Rim-Light Spotlight & Morphing `⌘K` Search Navbar

A dark or translucent glass navigation bar where hovering any link glides a **1px bottom laser rim-light** (`linear-gradient`) and a **soft upward spotlight cone** (`radial-gradient`) beneath the text, paired with an **expandable search input** that morphs from an icon button into a glowing search bar.

```html
<header class="relative flex items-center justify-between px-5 h-14 rounded-2xl bg-[#0D0D10]/90 backdrop-blur-xl border border-white/10 text-zinc-200 shadow-2xl overflow-hidden" id="rim-navbar">
  <!-- Sliding Bottom Rim-Light & Upward Spotlight Cone -->
  <div id="rim-spotlight" class="pointer-events-none absolute bottom-0 left-0 h-full w-28 opacity-0 transition-opacity duration-300" style="transform: translateX(0px);">
    <!-- Upward Spotlight Cone -->
    <div class="absolute inset-0 bg-[radial-gradient(50%_80%_at_50%_100%,rgba(239,68,68,0.28),transparent_80%)]"></div>
    <!-- 1px Bottom Laser Rim Line -->
    <div class="absolute bottom-0 inset-x-2 h-[2px] bg-gradient-to-r from-transparent via-red-500 to-transparent shadow-[0_0_12px_#ef4444]"></div>
  </div>

  <!-- Brand & Nav Links -->
  <div class="flex items-center gap-8 z-10">
    <a href="#" class="font-bold tracking-tight text-white flex items-center gap-2">
      <span class="w-2.5 h-2.5 rounded-sm bg-red-500 shadow-[0_0_10px_#ef4444]"></span>
      <span>PipWise</span>
    </a>
    <nav class="hidden md:flex items-center gap-1" id="rim-nav-links">
      <button class="rim-link px-3.5 py-2 text-xs font-medium text-zinc-300 hover:text-white transition-colors">Brokers</button>
      <button class="rim-link px-3.5 py-2 text-xs font-medium text-zinc-300 hover:text-white transition-colors">Reviews</button>
      <button class="rim-link px-3.5 py-2 text-xs font-medium text-zinc-300 hover:text-white transition-colors">Comparisons</button>
      <button class="rim-link px-3.5 py-2 text-xs font-medium text-zinc-300 hover:text-white transition-colors">Analytics</button>
    </nav>
  </div>

  <!-- Morphing Search Bar & Actions -->
  <div class="flex items-center gap-2.5 z-10">
    <div id="morph-search-box" class="relative flex items-center justify-end overflow-hidden rounded-xl border border-white/10 bg-white/5 transition-all duration-300 ease-[cubic-bezier(0.16,1,0.3,1)] w-9 h-9">
      <button id="morph-search-trigger" aria-label="Toggle Search" class="w-9 h-9 flex items-center justify-center text-zinc-400 hover:text-white shrink-0">
        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z"/></svg>
      </button>
      <input id="morph-search-input" type="text" placeholder="Search brokers, pairs..." class="w-full bg-transparent text-xs text-white placeholder-zinc-500 focus:outline-none pr-14 opacity-0 pointer-events-none transition-opacity duration-200" />
      <kbd id="morph-search-kbd" class="absolute right-2.5 px-1.5 py-0.5 text-[10px] font-mono bg-white/10 text-zinc-400 rounded opacity-0 pointer-events-none transition-opacity duration-200">⌘K</kbd>
    </div>
  </div>
</header>
```

```javascript
// Rim-Light Spotlight Tracking + Morphing Search Logic
function initRimNavbar() {
  const nav = document.getElementById('rim-navbar');
  const spotlight = document.getElementById('rim-spotlight');
  const links = document.querySelectorAll('.rim-link');
  const searchBox = document.getElementById('morph-search-box');
  const searchTrigger = document.getElementById('morph-search-trigger');
  const searchInput = document.getElementById('morph-search-input');
  const searchKbd = document.getElementById('morph-search-kbd');

  links.forEach((link) => {
    link.addEventListener('mouseenter', () => {
      const navRect = nav.getBoundingClientRect();
      const linkRect = link.getBoundingClientRect();
      const centerX = linkRect.left - navRect.left + linkRect.width / 2 - spotlight.offsetWidth / 2;
      spotlight.style.opacity = '1';
      if (window.gsap) {
        gsap.to(spotlight, { x: centerX, duration: 0.35, ease: 'power3.out' });
      } else {
        spotlight.style.transform = `translateX(${centerX}px)`;
      }
    });
  });

  nav.addEventListener('mouseleave', () => {
    spotlight.style.opacity = '0';
  });

  let searchOpen = false;
  const toggleSearch = (forceState) => {
    searchOpen = typeof forceState === 'boolean' ? forceState : !searchOpen;
    if (searchOpen) {
      searchBox.style.width = '250px';
      searchBox.classList.add('border-red-500/60', 'shadow-[0_0_15px_rgba(239,68,68,0.2)]');
      searchInput.classList.remove('opacity-0', 'pointer-events-none');
      searchKbd.classList.remove('opacity-0');
      searchInput.focus();
    } else {
      searchBox.style.width = '36px';
      searchBox.classList.remove('border-red-500/60', 'shadow-[0_0_15px_rgba(239,68,68,0.2)]');
      searchInput.classList.add('opacity-0', 'pointer-events-none');
      searchKbd.classList.add('opacity-0');
      searchInput.blur();
    }
  };

  searchTrigger.addEventListener('click', () => toggleSearch());
  window.addEventListener('keydown', (e) => {
    if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {
      e.preventDefault();
      toggleSearch(true);
    } else if (e.key === 'Escape' && searchOpen) {
      toggleSearch(false);
    }
  });
}
```

---

## Blueprint 3: Skeleton-to-Stagger Multi-View Switcher

When switching between major dashboard or app views (`Overview`, `Activity`, `Manage`, `Savings`), avoid abrupt DOM swaps. Instead:
1. Immediately show a **synchronized shimmer skeleton layout** (`260ms`).
2. Swap in the target view container and animate its child cards (`[data-stagger-card]`) upward with spring physics (`y: 18 -> 0, opacity: 0 -> 1, scale: 0.97 -> 1, stagger: 0.055`).

```javascript
function switchLivingView(targetViewId, skeletonOverlay, views) {
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduced) {
    views.forEach((v) => v.classList.toggle('hidden', v.id !== targetViewId));
    return;
  }

  // Step 1: Flash clean skeleton shimmer for 240ms
  skeletonOverlay.classList.remove('hidden', 'opacity-0');
  views.forEach((v) => v.classList.add('hidden'));

  setTimeout(() => {
    skeletonOverlay.classList.add('opacity-0');
    setTimeout(() => skeletonOverlay.classList.add('hidden'), 180);

    const activeView = document.getElementById(targetViewId);
    if (!activeView) return;
    activeView.classList.remove('hidden');

    // Step 2: Staggered spring entrance for all cards inside the new view
    const cards = activeView.querySelectorAll('[data-stagger-card]');
    if (window.gsap && cards.length) {
      gsap.fromTo(
        cards,
        { opacity: 0, y: 20, scale: 0.96 },
        {
          opacity: 1,
          y: 0,
          scale: 1,
          duration: 0.48,
          stagger: 0.055,
          ease: 'back.out(1.25)',
          clearProps: 'transform',
        }
      );
    }
  }, 240);
}
```

---

## Blueprint 4: Cinematic 000–100 Counter & FLIP Hero-to-Header Choreography

Ideal for luxury fashion (`Velvet`), creative studios, architectural portfolios, and flagship product launches:
1. **Stage 1 (000 $\to$ 100 Counter + Split Letter Reveal):** Warm editorial canvas with a central portrait cutout, a tabular `000` counter incrementing to `100`, and giant display letters revealing behind the portrait.
2. **Stage 2 (Full-Viewport Wordmark Dock):** At `100`, the brand wordmark scales cleanly to `100vw` at the top of the screen while the exposed `1px` hairline product grid slides into view from below.

```javascript
function runCinematicIntro({ counterEl, charsSelector, preloaderEl, heroWordmarkEl, gridCellsSelector }) {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches || !window.gsap) {
    if (preloaderEl) preloaderEl.style.display = 'none';
    return;
  }

  const counterObj = { val: 0 };
  const tl = gsap.timeline();

  // 1. Reveal oversized brand letters behind model cutout
  tl.fromTo(
    charsSelector,
    { yPercent: 110, opacity: 0 },
    { yPercent: 0, opacity: 1, duration: 0.7, stagger: 0.05, ease: 'expo.out' },
    0
  );

  // 2. Count 000 -> 100 with tabular precision
  tl.to(
    counterObj,
    {
      val: 100,
      duration: 1.4,
      ease: 'power2.inOut',
      onUpdate: () => {
        counterEl.textContent = String(Math.round(counterObj.val)).padStart(3, '0');
      },
    },
    0
  );

  // 3. Dock wordmark & curtain-lift preloader into the 1px hairline grid
  tl.to(preloaderEl, {
    yPercent: -100,
    duration: 0.75,
    ease: 'expo.inOut',
    onComplete: () => {
      preloaderEl.style.display = 'none';
    },
  });

  tl.fromTo(
    heroWordmarkEl,
    { scale: 0.75, y: 40, opacity: 0 },
    { scale: 1, y: 0, opacity: 1, duration: 0.7, ease: 'expo.out' },
    '-=0.45'
  );

  tl.fromTo(
    gridCellsSelector,
    { y: 48, opacity: 0 },
    { y: 0, opacity: 1, duration: 0.6, stagger: 0.06, ease: 'power3.out' },
    '-=0.5'
  );
}
```

---

## Blueprint 5: Interactive Spatial Product Stage & Pendulum Hanger Physics

Instead of displaying products only inside flat rectangles, create an **Interactive Showroom Stage** (inspired by Puma's hanging garment rack):
- Clicking any item on the rack centers and zooms it (`scale: 1.18`), pushes sibling items into soft depth-of-field blur (`scale: 0.88, opacity: 0.45`), and applies a **damped pendulum swing** (`rotation: 7 -> 0, ease: elastic.out(1, 0.35)`) around `transform-origin: 50% 0%` (the top hook).
- A hanging price/spec tag swings on a secondary phase (`rotation: -12 -> 0`).
- Clicking color swatches crossfades the garment colorway and triggers a subtle micro-swing.

```javascript
function selectStageGarment(itemEl, allItems, colorHex, titleEl, priceEl) {
  allItems.forEach((el) => {
    const isSelected = el === itemEl;
    if (window.gsap) {
      gsap.to(el, {
        scale: isSelected ? 1.15 : 0.88,
        opacity: isSelected ? 1 : 0.45,
        zIndex: isSelected ? 20 : 5,
        duration: 0.55,
        ease: 'expo.out',
      });
    }
  });

  // Pendulum swing around the top hanger hook (transform-origin: top center)
  const garmentBody = itemEl.querySelector('.garment-body');
  const hangTag = itemEl.querySelector('.hang-tag');
  if (window.gsap && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    gsap.fromTo(
      garmentBody,
      { rotation: 6.5, transformOrigin: '50% 0%' },
      { rotation: 0, duration: 1.35, ease: 'elastic.out(1, 0.32)' }
    );
    if (hangTag) {
      gsap.fromTo(
        hangTag,
        { rotation: -14, transformOrigin: '50% 0%' },
        { rotation: 0, duration: 1.6, ease: 'elastic.out(1, 0.25)' }
      );
    }
  }
}
```

---

## Blueprint 6: Exposed 1px Hairline Editorial Grid & Dual-Image Hover

For fashion, architecture, and design stores (`Velvet` archetype):
- Use an exposed `1px` border grid (`grid bg-stone-800 gap-[1px]` where each cell has `bg-stone-950` or `bg-stone-50`).
- Inside each cell, stack two images:
  1. **Primary Image:** Clean isolated garment/object packshot.
  2. **Secondary Hover Image:** Editorial model or in-context lifestyle photograph (`opacity-0 group-hover:opacity-100 group-hover:scale-105 transition-all duration-500`).
- Place the item title at the bottom-left and the `tabular-nums` price at the bottom-right in crisp monospace type.

---

## Blueprint 7: Living Telemetry Micro-Widgets (Dashboards & Fintech)

When building dashboards (`Cadra` / `Verde` archetypes), replace static numbers with interactive micro-widgets:

1. **10×10 Dot-Matrix Capacity Grid:**
   - Render 100 `6px × 6px` rounded dots in a `grid-cols-10 gap-1.5`.
   - Color the first $N$ dots with primary/secondary status hues (e.g., `48% Allocated` = 48 blue dots, 20 amber reserved dots, 32 muted available dots) and stagger their scale on tab load.
2. **Interactive SVG Area Chart with Hover Scrubber:**
   - Render smooth cubic-bezier `<path>` splines with a `<linearGradient>` fill below.
   - Bind `mousemove` on the SVG to move a vertical `1px` hairline cursor and position a frosted-glass tooltip showing exact `Revenue` vs `Cost` at that month.
3. **Semi-Circular Arc Gauge (`On-Time Delivery 91%`):**
   - Use an SVG `<path d="M 20 100 A 80 80 0 0 1 180 100" stroke-dasharray="251.2" stroke-dashoffset="22.6" />` and animate `strokeDashoffset` from `251.2` to `251.2 * (1 - pct / 100)` alongside a live `tabular-nums` counter.
4. **Tactile Card Controls (`Freeze`, `Show PIN`, `Spending Limit Slider`):**
   - Clicking **Freeze Card** toggles a frosted ice backdrop overlay (`backdrop-blur-md bg-sky-200/20`) over the metallic card and updates the status pill to `Frozen`.
   - Clicking **Show PIN** unblurs the `••••` digits (`filter: blur(5px) -> blur(0px)`).
   - Dragging the **Monthly Spending Limit** `<input type="range">` updates the formatted `$5,500.00` `tabular-nums` readout and progress fill bar at 60fps.

---

## Blueprint 8: 6-Layer Full-Screen Entrance & Automatic Leaf-Counter Cascade

In top-tier showcase interfaces (`Cadra` and `Vertix`), entering a page or switching tabs **never** just fades the outer container. Every visual layer cascades in from its natural vector while all numbers, bars, rings, and color fills animate from zero:

1. **Layer 1 — App Shell & Floating Docks (On Initial Load):**
   - Left floating dock slides in (`x: -28 -> 0`) while its icon buttons pop in (`scale: 0.3 -> 1, stagger: 0.03, ease: 'back.out(1.8)'`).
   - Top brand pill, center navbar track, and right utility pills glide in from top/sides.
2. **Layer 2 — Character-Wave Heading & CTA:**
   - Split the active view title into `<span class="char-slot">` elements and stagger from `{ opacity: 0, y: 20, filter: 'blur(4px)' }` to `{ opacity: 1, y: 0, filter: 'blur(0px)' }`.
3. **Layer 3 — Outer Cards (`y: 32, scale: 0.95 -> 0`):**
   - Stagger all primary cards (`stagger: 0.055, ease: 'power3.out'`).
4. **Layer 4 — Inner Wells, Rows & Sub-Headers (`y: 16, x: -12 -> 0`):**
   - Stagger inner boxes (`.v-well`, `.wh-header-box`, `.toggle-row`, `.sched-card`) with `delay: 0.06`.
5. **Layer 5 — Leaf Typography, Badges, Avatars & SKU Rows:**
   - Slide inner titles/labels (`x: -8, y: 10 -> 0`), pop avatars (`scale: 0.35 -> 1, ease: 'back.out(1.8)'`), and slide right-hand table/SKU rows from the right (`x: 22 -> 0`).
6. **Layer 6 — Color Fills, Bars, SVG Curves, Rings & Auto-Count-Up Numbers:**
   - Sweep horizontal bars (`scaleX: 0 -> 1`), grow vertical bars (`scaleY: 0 -> 1`), draw SVG curves/rings (`clipPath` / `strokeDashoffset`), and run `autoCountUpAllNumbers(activeView)` on every `.tabular-nums` leaf node so every dollar, percentage, and unit count animates from `0` to its target value.

---

## Blueprint 9: Tactile Builder & Live Receipt Stage (Tondo Pizza Pattern)

Ideal for restaurants, customizers, bakeries, configurators, and food ordering: replace boring menu grids with a **three-zone assembly workshop** — left ingredient palette grid, central open physical box/tray with tactile lid flip (`START YOUR ORDER`), and right tilted paper receipt (`rotate(1.6deg)`) pinned with a glossy 3D push-pin updating live in `tabular-nums` before a `Cook / Bake` state transformation.

> **Photorealistic Cutouts & State-Accurate Baking Rule (No Vector Icons / No Hardcoded Baked Photos)**: Never render ingredient palette cards or dropped pizza toppings with vector SVG icons/shapes, and never swap on `Cook` to a hardcoded photo containing unrequested toppings. Ground BOTH the palette tiles and dropped assembly layers in real `#FFFFFF`-isolated studio photographs passed through a border-seeded flood-fill alpha extractor (keeping interior white cheese/stems opaque while clearing outer white). Crossfade on `Cook` to a **bare baked base** (`baked-dough-sauce.jpg`: blistered crust + roasted tomato sauce ONLY) while keeping `#pizza-toppings-stage` visible on top so ONLY the user's selected layers transition to melted (`ing-mozzarella-baked.jpg`) or wood-roasted optics alongside the sliding quilted oven mitt.

```javascript
// Tactile Builder: Drop Topping onto Tray + Live Tabular-Nums Receipt + State Bake
function addIngredientToTray({ trayEl, receiptListEl, totalEl, item }) {
  const layer = document.createElement('div');
  layer.className = 'ingredient-layer pointer-events-none absolute inset-0 flex items-center justify-center';
  layer.innerHTML = item.svgOrCutoutMarkup;
  trayEl.appendChild(layer);

  if (window.gsap && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    gsap.fromTo(
      layer,
      { scale: 1.45, y: -28, rotation: gsap.utils.random(-14, 14), opacity: 0 },
      { scale: 1, y: 0, rotation: gsap.utils.random(-6, 6), opacity: 1, duration: 0.45, ease: 'back.out(1.6)' }
    );
  }

  const row = document.createElement('li');
  row.className = 'flex items-center justify-between text-xs py-1 border-b border-stone-200/70 tabular-nums';
  row.innerHTML = `<span>${item.name}</span><span>$${item.price.toFixed(2)}</span>`;
  receiptListEl.appendChild(row);
  totalEl.textContent = `$${computeReceiptTotal().toFixed(2)}`;
}
```

---

## Blueprint 10: Depth-of-Field Runway & Hotspot Bundle Drawer (Nike Try the Look Pattern)

Ideal for lookbooks, apparel campaigns, outfits, and curated multi-item bundles: display styled figures side-by-side; when one is selected, push siblings into **optical depth-of-field blur** (`blur(3px) opacity(0.62) scale(0.95)`), glide the focused figure left, pulse garment hotspots (`In This Look`), and slide in a **Complete the Look** bundle drawer with live `tabular-nums` subtotal calculation.

```css
.runway-figure {
  transition: transform 420ms cubic-bezier(0.16, 1, 0.3, 1),
              filter 380ms cubic-bezier(0.16, 1, 0.3, 1),
              opacity 320ms ease-out;
}
.runway-figure.is-dimmed {
  filter: blur(3px) saturate(0.75);
  opacity: 0.58;
  transform: scale(0.94);
}
.hotspot-pin::after {
  content: '';
  position: absolute;
  inset: -6px;
  border-radius: 999px;
  border: 1px solid currentColor;
  animation: hotspot-pulse 2.2s cubic-bezier(0.16, 1, 0.3, 1) infinite;
}
@keyframes hotspot-pulse {
  0% { transform: scale(0.8); opacity: 0.75; }
  100% { transform: scale(1.7); opacity: 0; }
}
```

---

## Blueprint 11: Cubby Shelf to SVG Anatomy Callout Stage (Oxide 10 Sneaker Pattern)

Ideal for footwear, industrial design, watches, hardware, and precision consumer products: present variants inside a structured **display cubby shelf**; clicking any cubby expands that SKU to center stage via FLIP/spring scale and draws **SVG leader lines** (`stroke-dashoffset`) pointing directly to physical regions (`UPPER MESH`, `SOLE UNIT`, `HEEL CLIP`).

```javascript
function revealAnatomyCallouts(stageEl) {
  const paths = stageEl.querySelectorAll('.leader-path');
  const cards = stageEl.querySelectorAll('.anatomy-card');
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  paths.forEach((p) => {
    const len = p.getTotalLength();
    p.style.strokeDasharray = len;
    p.style.strokeDashoffset = reduced ? 0 : len;
  });

  if (!window.gsap || reduced) return;
  const tl = gsap.timeline();
  tl.to(paths, { strokeDashoffset: 0, duration: 0.55, stagger: 0.08, ease: 'power3.out' })
    .fromTo(
      cards,
      { opacity: 0, y: 10, scale: 0.96 },
      { opacity: 1, y: 0, scale: 1, duration: 0.38, stagger: 0.07, ease: 'power3.out' },
      '-=0.3'
    );
}
```

---

## Blueprint 12: Live Ambient Physics & Kelvin Environment Stage (LUMEN & Kora Pattern)

Ideal for smart hardware, lighting, audio gear, specialty coffee, cosmetics, and sensory D2C brands: pair an obsidian or warm parchment canvas with **environmental physics controls** (`2700K–4000K` color temperature slider, intensity dimmer, or bottom origin selector tiles with an active `Selected` badge) that dynamically alter CSS custom properties (`--glow-rgb`, `--glow-alpha`) across the entire viewport.

```javascript
function updateKelvinEnvironment(stageRoot, kelvin) {
  // Smoothly interpolate between warm tungsten 2700K (255,176,94) and daylight 4000K (255,232,204)
  const ratio = Math.max(0, Math.min(1, (kelvin - 2700) / (4000 - 2700)));
  const g = Math.round(176 + ratio * 56);
  const b = Math.round(94 + ratio * 110);
  stageRoot.style.setProperty('--ambient-glow-rgb', `255, ${g}, ${b}`);
  const readout = stageRoot.querySelector('[data-kelvin-readout]');
  if (readout) readout.textContent = `${kelvin}K`;
}
```

---

## Blueprint 13: Boutique / Locker Rail Glide & Slide-Over Checkout Flow (Timnas / ORZR / Moda Rebr)

Ideal for apparel collections, team rosters, and multi-category boutiques (`CLOTHING / ACCESSORY` rail switches): siblings part horizontally on pointer hover; clicking pulls the item onto the studio stage with a **Front / Back flip toggle**, size pill selector, and a slide-over **Bag → Checkout → Order Placed** drawer flow using `slidePill` / spring transitions.

```javascript
function bindRailPartingPhysics(railItems) {
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  railItems.forEach((item, idx) => {
    item.addEventListener('mouseenter', () => {
      if (reduced || !window.gsap) return;
      railItems.forEach((sib, sIdx) => {
        const offset = sIdx === idx ? 0 : (sIdx < idx ? -14 : 14);
        gsap.to(sib, {
          x: offset,
          scale: sIdx === idx ? 1.07 : 0.96,
          duration: 0.35,
          ease: 'power3.out',
        });
      });
    });
    item.addEventListener('mouseleave', () => {
      if (reduced || !window.gsap) return;
      gsap.to(railItems, { x: 0, scale: 1, duration: 0.42, ease: 'power3.out' });
    });
  });
}
```


