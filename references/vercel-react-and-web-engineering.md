# Vercel React, Next.js Performance & Composition Engineering

Distilled from **Vercel Engineering (`agent-skills`)** covering Next.js App Router, React 19, bundle architecture, Server Components, client re-render hygiene, and Core Web Vitals (`LCP < 2.5s`, `CLS < 0.1`, `INP < 200ms`). Load whenever implementing or auditing React/Next.js applications.

---

## 1. Eight Priority Tiers of React & Next.js Performance

### Tier 1 — Eliminating Waterfalls (`CRITICAL`)
- `async-parallel`: Run independent I/O in parallel via `Promise.all()` or `Promise.allSettled()`, never sequential `await` chains.
- `async-defer-await`: Move `await` into the exact conditional branch that consumes the result; return early on cheap synchronous guards before awaiting remote calls (`async-cheap-condition-before-await`).
- `async-api-routes`: Initiate promises immediately at the top of API routes/loaders and `await` only right before response serialization.
- `async-suspense-boundaries`: Wrap independent async RSC data regions in `<Suspense fallback={<Skeleton />}>` to stream shells without blocking the whole route.

### Tier 2 — Bundle Size Optimization (`CRITICAL`)
- `bundle-barrel-imports`: Import leaf modules directly (e.g., `lucide-react/dist/esm/icons/...` or package subpath imports) instead of re-exporting barrels that pull entire icon/utility graphs.
- `bundle-dynamic-imports`: Lazy-load heavy visualization, WebGL/3D, rich-text editors, or modal-only views via `next/dynamic` (`{ ssr: false }` where browser-only).
- `bundle-defer-third-party` & `bundle-conditional`: Defer non-critical analytics/telemetry after hydration and load heavy feature code only when triggered; preload on `onMouseEnter`/`onFocus` (`bundle-preload`).

### Tier 3 — Server-Side & RSC Performance (`HIGH`)
- `server-auth-actions`: Always authenticate and authorize **inside** every Server Action — never assume page middleware alone guards action endpoints.
- `server-serialization`: Pass minimal primitive/serialized subsets across `"use client"` boundaries; never serialize full ORM records or secret columns to Client Components.
- `server-cache-react`: Wrap shared per-request queries/loaders in `React.cache(...)` for single-render deduplication; avoid module-level mutable request state (`server-no-shared-module-state`).
- `server-hoist-static-io` & `server-after-nonblocking`: Hoist static schema/asset metadata at module load; offload logging/webhooks with Next.js `after()`.

### Tier 4 — Client Data & Event Listeners (`MEDIUM-HIGH`)
- Use request deduplication (`SWR` / React Query) rather than raw `useEffect` + `fetch` waterfalls.
- Deduplicate global window listeners and mark scroll/touch/wheel listeners `{ passive: true }`.
- Version `localStorage` keys cleanly and keep client cache reads cached in memory during hot loops.

### Tier 5 — Re-Render Optimization (`MEDIUM`)
- `rerender-derived-state-no-effect`: Compute derived booleans/totals synchronously during render (`const total = items.reduce(...)`), **never** via `useState` + `useEffect`.
- `rerender-use-ref-transient-values`: **Never drive high-frequency pointer, scroll, or animation ticks through React state.** Keep mutable coordinates/rAF IDs in `useRef` and update DOM transforms directly.
- `rerender-defer-reads` & `rerender-functional-setstate`: Do not subscribe a component to state read only inside event callbacks; use functional updates `setItems(prev => ...)` for stable callback identities.
- `rerender-transitions` & `rerender-use-deferred-value`: Wrap non-urgent filter/tab updates in `startTransition` or `useDeferredValue` so typing stays `< 16ms/frame`.
- `rerender-no-inline-components`: Never declare component functions (`const Row = () => ...`) inside another component's render body (destroys DOM state & remounts every render).

### Tier 6 & Tier 7 — Rendering & JavaScript Micro-Performance
- `rendering-animate-svg-wrapper`: Animate an outer `<div>` wrapper rather than mutating `<svg>` transforms directly to keep GPU compositing fast.
- `rendering-content-visibility`: Add `content-visibility: auto; contain-intrinsic-size: ...` on long lists/logs ($50+$ rows or virtualize).
- `rendering-conditional-render`: Use explicit ternaries `cond ? <Node /> : null` rather than `count && <Node />` (prevents stray `0` text leaks).
- `js-index-maps` & `js-tosorted-immutable`: Build `new Map()` / `new Set()` lookups instead of repeated `.find()` scans inside loops; use `.toSorted()` instead of mutating `.sort()`.

---

## 2. Scalable Component Composition Patterns & React 19 APIs

1. **Avoid Boolean Prop Proliferation (`architecture-avoid-boolean-props`):**
   - *Anti-pattern:* `<Card compact elevated withHeader darkBorder showFooter />` — exponentially fragments code paths.
   - *Pattern:* Compose explicit children/slots (`<Card.Root><Card.Header /><Card.Body /></Card.Root>`) or explicit semantic variant components (`patterns-explicit-variants`).
2. **Compound Components + Decoupled State (`architecture-compound-components`):**
   - Lift shared state into a root Provider exporting `{ state, actions, meta }` (`state-context-interface`), decoupling *where* state lives (`state-decouple-implementation`: local state, URL params, server sync) from visual child parts (`Trigger`, `List`, `Item`).
3. **Prefer `children` Over `renderX` Props (`patterns-children-over-render-props`):**
   - Compose UI slots declaratively via JSX `children` rather than stringing multiple `renderHeader`, `renderRow`, `renderEmpty` callback props.
4. **React 19 Conventions (when `package.json` specifies React 19+):**
   - Pass `ref` directly as a normal component prop (`function Input({ ref, ...props })`) — do not wrap new components in `React.forwardRef`.
   - Read Context conditionally or unwrap promises cleanly with `use(Context)` instead of `useContext(Context)`.

---

## 3. Core Web Vitals 9 Delivery Levers (`LCP < 2.5s`, `CLS < 0.1`, `INP < 200ms`)

1. Acknowledge pointer actions `< 100ms` (optimistic state + subtle skeletons over blocking full-page spinners).
2. Split heavy routes/charts dynamically; keep initial JS payload minimal.
3. Inline critical above-the-fold styles; preload hero LCP font/image (`fetchpriority="high"`).
4. Keep static layout shells in RSC/SSR; hydrate interactive leaves only.
5. Lazy-load below-fold images/media (`loading="lazy"`).
6. Keep main thread `< 16ms/frame`; debounce heavy searches (`150–250ms`), keep scroll listeners passive.
7. Lock explicit `width`/`height` or `aspect-ratio` on every `<img>`, `<video>`, and async slot (`CLS < 0.1`).
8. Serve WebP/AVIF cutouts/assets (`< 150 KB` per preview, responsive `sizes`).
9. Cache immutable hashed assets aggressively at CDN edge.
