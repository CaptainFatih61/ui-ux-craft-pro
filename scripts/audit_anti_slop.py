#!/usr/bin/env python3
"""
Anti-AI Slop & High-Craft UX Automated Audit Script
Zero external dependencies. Scans codebases for generic AI artifacts, accessibility regressions,
concentric radius mistakes, and optical styling violations.
"""

import os
import sys
import re
import argparse
from pathlib import Path

# ANSI Color codes
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

SLOP_GRADIENTS = [
    (re.compile(r"from-purple-[456]00\s+to-indigo-[456]00", re.I), "Generic AI purple-to-indigo gradient cliché"),
    (re.compile(r"from-violet-[456]00\s+to-indigo-[456]00", re.I), "Generic AI violet-to-indigo gradient cliché"),
    (re.compile(r"from-indigo-[456]00\s+to-purple-[456]00", re.I), "Generic AI indigo-to-purple gradient cliché"),
    (re.compile(r"from-pink-[456]00\s+to-purple-[456]00", re.I), "Generic AI pink-to-purple gradient cliché"),
    (re.compile(r"#6366f1", re.I), "Default Tailwind indigo-500 hardcoded (#6366f1)"),
    (re.compile(r"#8b5cf6", re.I), "Default Tailwind violet-500 hardcoded (#8b5cf6)"),
    (re.compile(r"#667eea", re.I), "Infamous 2018 Canva/AI purple gradient token (#667eea)"),
]

SLOP_COPYWRITING = [
    (re.compile(r"\b10x\s+faster\b", re.I), "Generic AI hype copy cliché ('10x faster')"),
    (re.compile(r"\b10\s*kat\s*h[ıi]zland[ıi]r", re.I), "Generic Turkish AI hype copy cliché ('10 kat hızlandır')"),
    (re.compile(r"\bunleash\s+the\s+power\b", re.I), "Generic AI hype copy cliché ('Unleash the power')"),
    (re.compile(r"\brevolutionize\s+your\b", re.I), "Generic AI hype copy cliché ('Revolutionize your')"),
    (re.compile(r"\bsupercharge\s+your\b", re.I), "Generic AI hype copy cliché ('Supercharge your')"),
    (re.compile(r"\bstreamline\s+your\s+workflow\b", re.I), "Generic AI hero headline cliché ('Streamline your workflow')"),
    (re.compile(r"\blike\s+never\s+before\b", re.I), "Generic AI hype copy cliché ('Like never before')"),
    (re.compile(r"\bempower\s+your\b", re.I), "Generic AI hype copy cliché ('Empower your')"),
    (re.compile(r"\bnext-gen\s+platform\b", re.I), "Generic AI hype copy cliché ('Next-gen platform')"),
    (re.compile(r"\bseamless\s+solutions?\b", re.I), "Generic AI hype copy cliché ('Seamless solutions')"),
    (re.compile(r"\belevate\s+your\s+workflow\b", re.I), "Generic AI hype copy cliché ('Elevate your workflow')"),
    (re.compile(r"\bwelcome\s+back,\s*Alex\b", re.I), "Generic SaaS workbench welcome banner cliché ('Welcome back, Alex')"),
    (re.compile(r">\s*(?:Hero\s+Section|Bento\s+Grid)\s*<", re.I), "Visible prompt meta-leakage label rendered in DOM"),
    (re.compile(r"\b(?:SaaSify|NexusAI|AetherFlow)\b", re.I), "Generic AI SaaS brand cliché"),
    (re.compile(r"\bAlex\s+Chen\b", re.I), "Generic AI placeholder persona cliché ('Alex Chen')"),
]

SURFACE_SLOP_CHECKS = [
    (re.compile(r"\bborder-[lt]-(?:[3-9]|\[\d+px\])\b"), "Decorative thick colored side/top card stripe (Tailwind border-l/t)"),
    (re.compile(r"border-(?:left|top):\s*[3-9]\d*px\s+solid", re.I), "Decorative thick colored side/top stripe (use 1px full outline or dot)"),
    (re.compile(r"box-shadow:\s*0(?:px)?\s+0(?:px)?\s+(?:1[6-9]|[2-9]\d)px\b", re.I), "Zero-offset neon glow box-shadow (use physical offset depth)"),
]

ROBOTIC_TRANSITIONS = [
    (re.compile(r"transition:\s*all\b(?![^;]*cubic-bezier)", re.I), "Generic 'transition: all' without asymmetric cubic-bezier spring timing"),
    (re.compile(r"\btransition-all\b(?![^\"'>]*ease-\[cubic-bezier)", re.I), "Generic Tailwind 'transition-all' without explicit cubic-bezier ease"),
]

MOTION_ENGINE_MARKER = re.compile(r"\b(?:gsap|@keyframes|cubic-bezier|requestAnimationFrame)\b", re.I)

ACCESSIBILITY_CHECKS = [
    (re.compile(r"<button\b(?![^>]*aria-label)(?![^>]*aria-labelledby)[^>]*>\s*<svg", re.I), "Icon-only button missing aria-label"),
    (re.compile(r"<img\b(?![^>]*\balt=)[^>]*>", re.I), "Image tag missing alt attribute"),
    (re.compile(r"user-scalable\s*=\s*no", re.I), "Viewport meta disables user scaling (accessibility violation)"),
    (re.compile(r'tabindex\s*=\s*["\'][1-9]', re.I), "Positive tabindex breaks natural keyboard focus order (use 0 or -1)"),
]

PRICE_TABULAR_CHECK = re.compile(r"(?:[\$\€\£\₺]|USD|EUR)\s*\d+[\d\.,]*")

def audit_file(filepath: Path):
    violations = []
    warnings = []
    
    try:
        content = filepath.read_text(encoding="utf-8", errors="ignore")
    except Exception as e:
        return violations, warnings

    lines = content.splitlines()

    for i, line in enumerate(lines, 1):
        # 1. Slop gradients & hex checks
        for pattern, desc in SLOP_GRADIENTS:
            if pattern.search(line):
                violations.append((i, "SLOP_GRADIENT", desc, line.strip()))

        # 1b. AI cliché copywriting checks
        for pattern, desc in SLOP_COPYWRITING:
            if pattern.search(line):
                warnings.append((i, "SLOP_COPYWRITING", desc, line.strip()[:80]))

        # 1c. Surface slop checks (side stripe / zero-offset neon glow)
        for pattern, desc in SURFACE_SLOP_CHECKS:
            if pattern.search(line):
                warnings.append((i, "SURFACE_SLOP", desc, line.strip()[:80]))

        # 1d. Horizontal overflow without overflow-y:hidden triggers phantom cross-axis scrollbars
        if re.search(r"overflow-x\s*:\s*auto\b", line, re.I):
            ctx = " ".join(lines[max(0, i - 5):min(len(lines), i + 5)])
            if not re.search(r"overflow-y\s*:\s*hidden|scrollbar-width\s*:\s*none", ctx, re.I):
                warnings.append((i, "PHANTOM_SCROLLBAR", "overflow-x: auto without overflow-y: hidden or scrollbar-width: none", line.strip()[:80]))

        # 1e. Robotic transition checks
        for pattern, desc in ROBOTIC_TRANSITIONS:
            if pattern.search(line):
                warnings.append((i, "ROBOTIC_TRANSITION", desc, line.strip()[:80]))

        # 1f. React 19 composition check (prefer ref prop over legacy forwardRef)
        if filepath.suffix.lower() in {".tsx", ".jsx"} and re.search(r"\bforwardRef\s*\(", line):
            warnings.append((i, "REACT19_FORWARD_REF", "React 19 prefers direct ref prop instead of React.forwardRef wrapper", line.strip()[:80]))

        # 2. Accessibility checks
        for pattern, desc in ACCESSIBILITY_CHECKS:
            if pattern.search(line):
                violations.append((i, "A11Y_DEFECT", desc, line.strip()[:80]))

        # 2b. Outline-none without ring check
        if "outline-none" in line:
            if not ("ring" in line or "focus" in line or "border" in line):
                violations.append((i, "A11Y_DEFECT", "outline-none used without visible focus replacement (ring/border)", line.strip()[:80]))

        # 3. Currency without tabular nums
        if PRICE_TABULAR_CHECK.search(line):
            if "tabular-nums" not in line and "font-variant-numeric" not in line:
                # Check surrounding lines (within 2 lines)
                context_window = " ".join(lines[max(0, i-3):min(len(lines), i+2)])
                if "tabular-nums" not in context_window and "font-variant-numeric" not in context_window:
                    warnings.append((i, "OPTICS_TABULAR", "Price/currency rendered without tabular-nums (may cause layout jitter)", line.strip()[:80]))

    # File-level checks for HTML
    if filepath.suffix.lower() == ".html":
        if "<meta" in content and "viewport" in content:
            if "width=device-width" not in content:
                violations.append((1, "A11Y_VIEWPORT", "HTML missing width=device-width in viewport meta tag", ""))
        elif "<html" in content and "<body" in content:
            violations.append((1, "A11Y_VIEWPORT", "HTML missing viewport meta tag entirely", ""))
        if "<body" in content and not MOTION_ENGINE_MARKER.search(content):
            warnings.append((1, "DEAD_STATIC_PAGE", "HTML has no living motion/spring engine (gsap, @keyframes, cubic-bezier, or requestAnimationFrame)", ""))
        if re.search(r"<h1\b", content, re.I) and re.search(r"<h3\b", content, re.I) and not re.search(r"<h2\b", content, re.I):
            warnings.append((1, "SKIPPED_HEADING", "HTML jumps from <h1> to <h3> without an intervening <h2>", ""))
        svg_primitives = len(re.findall(r"<(?:circle|ellipse)\b", content, re.I))
        has_large_stage_svg = bool(re.search(r'viewBox=["\']0\s+0\s+[3-9]\d\d\s+[3-9]\d\d["\']', content))
        has_photo_img = bool(re.search(r"<img\b[^>]+src=", content, re.I))
        if has_large_stage_svg and svg_primitives >= 8 and not has_photo_img:
            warnings.append((1, "CARTOON_SVG_STAGE", "Large stage SVG uses primitive <circle>/<ellipse> shapes without any photorealistic <img> studio assets", ""))

    return violations, warnings

def main():
    parser = argparse.ArgumentParser(description="Audit codebase for AI slop, accessibility regressions, and craft defects.")
    parser.add_argument("target", nargs="?", default=".", help="Directory or file to audit (default: .)")
    parser.add_argument("--strict", action="store_true", help="Fail on warnings as well as violations")
    args = parser.parse_args()

    target_path = Path(args.target).resolve()
    extensions = {".html", ".htm", ".jsx", ".tsx", ".vue", ".svelte", ".css", ".php"}

    if target_path.is_file():
        files_to_check = [target_path]
    else:
        files_to_check = []
        for root, dirs, files in os.walk(target_path):
            # Ignore common non-target dirs
            dirs[:] = [d for d in dirs if d not in {".git", "node_modules", ".claude", "dist", "build", "coverage", ".antigravity"}]
            for f in files:
                p = Path(root) / f
                if p.suffix.lower() in extensions:
                    files_to_check.append(p)

    total_violations = 0
    total_warnings = 0
    clean_files = 0

    print(f"\n{BOLD}{CYAN}=== High-Craft UX & Anti-Slop Audit Engine ==={RESET}")
    print(f"Scanning target: {target_path}")
    print(f"Discovered {len(files_to_check)} visual frontend files to audit.\n")

    for f in sorted(files_to_check):
        rel_path = f.relative_to(target_path) if target_path.is_dir() else f.name
        violations, warnings = audit_file(f)

        if violations or warnings:
            print(f"{BOLD}File: {rel_path}{RESET}")
            for line_no, category, desc, snippet in violations:
                total_violations += 1
                print(f"  {RED}[VIOLATION]{RESET} L{line_no} [{category}]: {desc}")
                if snippet:
                    print(f"    Snippet: {snippet}")
            for line_no, category, desc, snippet in warnings:
                total_warnings += 1
                print(f"  {YELLOW}[WARNING]{RESET}   L{line_no} [{category}]: {desc}")
                if snippet:
                    print(f"    Snippet: {snippet}")
            print()
        else:
            clean_files += 1

    print(f"{BOLD}=== Audit Summary ==={RESET}")
    print(f"Files audited:      {len(files_to_check)}")
    print(f"Pristine files:     {GREEN}{clean_files}{RESET}")
    print(f"Total Violations:   {RED if total_violations else GREEN}{total_violations}{RESET}")
    print(f"Total Warnings:     {YELLOW if total_warnings else GREEN}{total_warnings}{RESET}")

    if total_violations > 0 or (args.strict and total_warnings > 0):
        print(f"\n{RED}{BOLD}FAILED:{RESET} Fix the reported defects before production release.\n")
        sys.exit(1)
    else:
        print(f"\n{GREEN}{BOLD}PASSED:{RESET} Interface code adheres to high-craft optical and accessibility standards!\n")
        sys.exit(0)

if __name__ == "__main__":
    main()
