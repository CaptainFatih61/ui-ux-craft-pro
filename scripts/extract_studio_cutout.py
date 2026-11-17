#!/usr/bin/env python3
"""
Neural Studio Cutout & Contact-Sheet Utility for Physical / Apparel Stages.

Extracts clean RGBA cutouts from studio photography or foreground-sharp (d=0) video
frames using rembg (u2net_human_seg + isnet-general-use + u2net) with RGB edge
decontamination (distance_transform_edt) and interior-only sharpening so white
garments never puncture and dark denim never retains bright edge halos.

Recommended invocation:
    uv run --with pillow --with numpy --with opencv-python-headless --with rembg \
      --with onnxruntime --with scipy python scripts/extract_studio_cutout.py \
      input.png output.png --mode model --target-height 1100 --contact-sheet sheet.png
"""

from __future__ import annotations

import argparse
import pathlib
import sys


def parse_crop(raw: str | None) -> tuple[float, float, float, float] | None:
    if not raw:
        return None
    parts = [float(p.strip()) for p in raw.split(",")]
    if len(parts) != 4:
        raise argparse.ArgumentTypeError("Crop must be four comma-separated fractions: x1,y1,x2,y2")
    x1, y1, x2, y2 = parts
    if not (0.0 <= x1 < x2 <= 1.0 and 0.0 <= y1 < y2 <= 1.0):
        raise argparse.ArgumentTypeError("Crop fractions must satisfy 0 <= x1 < x2 <= 1 and 0 <= y1 < y2 <= 1")
    return x1, y1, x2, y2


def crop_fractional(pil_img, box: tuple[float, float, float, float]):
    w, h = pil_img.size
    fx1, fy1, fx2, fy2 = box
    return pil_img.crop((int(fx1 * w), int(fy1 * h), int(fx2 * w), int(fy2 * h)))


def remove_floor_gaps_between_legs(rgb, alpha_u8):
    """Suppress neutral studio cyclorama floor trapped between trouser legs/ankles."""
    import numpy as np

    h, _ = alpha_u8.shape
    out = alpha_u8.copy()
    y_start = int(h * 0.68)
    for y in range(y_start, h):
        row_fg = np.where(out[y] > 40)[0]
        if len(row_fg) < 20:
            continue
        x_left = int(row_fg.min()) + 8
        x_right = int(row_fg.max()) - 8
        if x_right <= x_left:
            continue
        sub_rgb = rgb[y, x_left:x_right].astype(np.int16)
        mx = sub_rgb.max(axis=1)
        mn = sub_rgb.min(axis=1)
        floor_like = (mn > 178) & ((mx - mn) < 16)
        floor_like = floor_like & ((y < int(h * 0.91)) | (mn < 228))
        if np.any(floor_like):
            xs_clear = np.where(floor_like)[0] + x_left
            out[y, xs_clear] = 0
    return out


def decontaminate_rgb_edges(rgb, alpha_u8, erode_px: int = 3, lower_erode_y_frac: float | None = None):
    """Replace semi-transparent fringe RGB with nearest eroded solid foreground pixel."""
    import cv2
    import numpy as np
    from scipy import ndimage

    h = alpha_u8.shape[0]
    solid_top = cv2.erode(
        (alpha_u8 >= 235).astype(np.uint8),
        cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (erode_px, erode_px)),
        iterations=1,
    ) > 0
    solid_mask = solid_top
    if lower_erode_y_frac is not None:
        solid_bot = cv2.erode(
            (alpha_u8 >= 242).astype(np.uint8),
            cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)),
            iterations=2,
        ) > 0
        split_y = int(lower_erode_y_frac * h)
        solid_mask = solid_top.copy()
        solid_mask[split_y:, :] = solid_bot[split_y:, :]

    if not np.any(solid_mask):
        return rgb

    idx_y, idx_x = ndimage.distance_transform_edt(~solid_mask, return_distances=False, return_indices=True)
    nearest_rgb = rgb[idx_y, idx_x]
    blend = np.clip((248.0 - alpha_u8.astype(np.float32)) / 95.0, 0.0, 1.0)[:, :, None]
    clean = rgb.astype(np.float32) * (1.0 - blend) + nearest_rgb.astype(np.float32) * blend
    return np.clip(clean, 0, 255).astype(np.uint8)


def extract_model_cutout(
    pil_crop,
    mode: str,
    target_h: int = 1100,
    pad: int = 12,
    clean_leg_floor: bool = True,
):
    import cv2
    import numpy as np
    from PIL import Image
    from rembg import new_session, remove

    rgb = np.array(pil_crop.convert("RGB"), dtype=np.uint8)
    human_sess = new_session("u2net_human_seg")
    isnet_sess = new_session("isnet-general-use")

    a_h = np.array(remove(pil_crop.convert("RGB"), session=human_sess), dtype=np.uint8)[:, :, 3].astype(np.float32)
    a_i = np.array(remove(pil_crop.convert("RGB"), session=isnet_sess), dtype=np.uint8)[:, :, 3].astype(np.float32)

    if mode == "white-garment":
        u2_sess = new_session("u2net")
        a_u = np.array(remove(pil_crop.convert("RGB"), session=u2_sess), dtype=np.uint8)[:, :, 3].astype(np.float32)
        alpha = a_i.copy()
        hm = alpha.shape[0]
        # Preserve white sneaker soles and lower denim contour while eroding dark-denim edge halo
        alpha[int(0.89 * hm):, :] = np.maximum(alpha[int(0.89 * hm):, :], a_u[int(0.89 * hm):, :])
        denim_y = int(0.38 * hm)
        alpha[denim_y:, :] = cv2.erode(
            alpha[denim_y:, :], cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)), iterations=1
        )
        # Retain opaque core white upper garment where human_seg identifies the garment clearly
        alpha[:denim_y, :] = np.where(a_h[:denim_y, :] > 205, np.maximum(alpha[:denim_y, :], a_h[:denim_y, :]), alpha[:denim_y, :])
        alpha_u8 = np.clip((alpha - 42.0) * (255.0 / (238.0 - 42.0)), 0.0, 255.0).astype(np.uint8)
        alpha_u8 = cv2.GaussianBlur(alpha_u8, (3, 3), 0.6)
        rgb = decontaminate_rgb_edges(rgb, alpha_u8, erode_px=3, lower_erode_y_frac=0.38)
    else:
        alpha = np.where(a_h > 200, np.maximum(a_h * 0.7 + a_i * 0.3, a_h * 0.85), np.minimum(a_h, a_i * 0.85 + 35.0))
        alpha = np.clip((alpha - 36.0) * (255.0 / (238.0 - 36.0)), 0.0, 255.0)
        alpha = cv2.GaussianBlur(alpha, (3, 3), 0.55)
        alpha_u8 = np.clip(alpha, 0, 255).astype(np.uint8)
        if clean_leg_floor:
            alpha_u8 = remove_floor_gaps_between_legs(rgb, alpha_u8)
        rgb = decontaminate_rgb_edges(rgb, alpha_u8, erode_px=3)

    mask_bin = (alpha_u8 > 28).astype(np.uint8)
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(mask_bin, connectivity=8)
    _, w = alpha_u8.shape
    if num_labels > 1:
        max_area = stats[1:, cv2.CC_STAT_AREA].max()
        keep = np.zeros_like(alpha_u8)
        for lbl in range(1, num_labels):
            area = stats[lbl, cv2.CC_STAT_AREA]
            cx = centroids[lbl][0]
            if area >= max_area * 0.30 or (area >= max_area * 0.02 and 0.16 * w <= cx <= 0.84 * w):
                keep[labels == lbl] = 255
        alpha_u8 = np.where(keep > 0, alpha_u8, 0).astype(np.uint8)

    ys, xs = np.where(alpha_u8 > 14)
    if len(ys) == 0:
        return Image.fromarray(np.dstack([rgb, alpha_u8]), mode="RGBA")
    y1, y2 = int(ys.min()), int(ys.max()) + 1
    x1, x2 = int(xs.min()), int(xs.max()) + 1
    rgb_crop = rgb[y1:y2, x1:x2]
    a_crop = alpha_u8[y1:y2, x1:x2]

    ch, cw = rgb_crop.shape[:2]
    if ch < 700:
        bgr = cv2.cvtColor(rgb_crop, cv2.COLOR_RGB2BGR)
        enhanced = cv2.detailEnhance(bgr, sigma_s=5, sigma_r=0.07)
        bgr = cv2.addWeighted(bgr, 0.65, enhanced, 0.35, 0)
        rgb_crop = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)

    inner_h = max(1, target_h - 2 * pad)
    scale = inner_h / float(ch)
    inner_w = max(1, int(round(cw * scale)))

    rgb_up = cv2.resize(rgb_crop, (inner_w, inner_h), interpolation=cv2.INTER_LANCZOS4)
    a_up = cv2.resize(a_crop, (inner_w, inner_h), interpolation=cv2.INTER_LANCZOS4)

    # Sharpen interior only so outer edges never develop unsharp-mask overshoot halos
    blur = cv2.GaussianBlur(rgb_up, (0, 0), 1.0)
    rgb_sharp = cv2.addWeighted(rgb_up, 1.32, blur, -0.32, 0)
    interior = cv2.erode((a_up >= 248).astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)), iterations=1)
    rgb_final = np.where(interior[:, :, None] > 0, rgb_sharp, rgb_up)

    out_w = inner_w + 2 * pad
    canvas = np.zeros((target_h, out_w, 4), dtype=np.uint8)
    canvas[pad:pad + inner_h, pad:pad + inner_w, :3] = rgb_final
    canvas[pad:pad + inner_h, pad:pad + inner_w, 3] = a_up
    return Image.fromarray(canvas, mode="RGBA")


def extract_packshot_cutout(
    pil_crop,
    size: int = 320,
    pad: int = 18,
    fill_holes: bool = False,
    symmetrize_x: bool = False,
    use_u2net: bool = False,
):
    import cv2
    import numpy as np
    from PIL import Image
    from rembg import new_session, remove

    rgb = np.array(pil_crop.convert("RGB"), dtype=np.uint8)
    session = new_session("u2net" if use_u2net else "isnet-general-use")
    alpha_u8 = np.array(remove(pil_crop.convert("RGB"), session=session), dtype=np.uint8)[:, :, 3]
    alpha_u8 = np.clip((alpha_u8.astype(np.float32) - 24.0) * (255.0 / (238.0 - 24.0)), 0.0, 255.0).astype(np.uint8)

    if symmetrize_x:
        mid = alpha_u8.shape[1] // 2
        alpha_u8[:, mid:mid * 2] = np.fliplr(alpha_u8[:, :mid])
        top_h = int(rgb.shape[0] * 0.34)
        rgb[:top_h, mid:mid * 2] = np.fliplr(rgb[:top_h, :mid])

    if fill_holes:
        corners = np.vstack([
            rgb[0:3, 0:3].reshape(-1, 3),
            rgb[0:3, -3:].reshape(-1, 3),
            rgb[-3:, 0:3].reshape(-1, 3),
            rgb[-3:, -3:].reshape(-1, 3),
        ])
        bg_med = np.median(corners, axis=0)
        dist = np.linalg.norm(rgb.astype(np.float32) - bg_med[None, None, :], axis=2)
        fg_raw = ((alpha_u8 > 55) | (dist > 19.0)).astype(np.uint8) * 255
        nl, lbls, st, _ = cv2.connectedComponentsWithStats((fg_raw > 0).astype(np.uint8), connectivity=8)
        if nl > 1:
            max_lbl = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
            fg_raw = np.where(lbls == max_lbl, 255, 0).astype(np.uint8)
        closed = cv2.morphologyEx(fg_raw, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9)))
        # Clear outer 2px border so exterior floodfill wraps around footwear touching crop edges
        closed[:2, :] = 0
        closed[-2:, :] = 0
        closed[:, :2] = 0
        closed[:, -2:] = 0
        h_m, w_m = closed.shape
        ff = closed.copy()
        mask_ff = np.zeros((h_m + 2, w_m + 2), np.uint8)
        cv2.floodFill(ff, mask_ff, (0, 0), 255)
        holes = cv2.bitwise_not(ff)
        repaired = cv2.bitwise_or(closed, holes)
        repaired_soft = cv2.GaussianBlur(repaired.astype(np.float32), (3, 3), 0.7)
        alpha_u8 = np.maximum(alpha_u8, repaired_soft.astype(np.uint8))

    mask_bin = (alpha_u8 > 24).astype(np.uint8)
    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(mask_bin, connectivity=8)
    if num_labels > 1:
        largest_lbl = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
        max_area = stats[largest_lbl, cv2.CC_STAT_AREA]
        keep = np.zeros_like(alpha_u8)
        for lbl in range(1, num_labels):
            if stats[lbl, cv2.CC_STAT_AREA] >= max_area * 0.15:
                keep[labels == lbl] = 255
        alpha_u8 = np.where(keep > 0, alpha_u8, 0).astype(np.uint8)

    rgb = decontaminate_rgb_edges(rgb, alpha_u8, erode_px=3)

    ys, xs = np.where(alpha_u8 > 14)
    if len(ys) == 0:
        return Image.new("RGBA", (size, size), (0, 0, 0, 0))
    y1, y2 = int(ys.min()), int(ys.max()) + 1
    x1, x2 = int(xs.min()), int(xs.max()) + 1
    rgb_c = rgb[y1:y2, x1:x2]
    a_c = alpha_u8[y1:y2, x1:x2]

    ch, cw = rgb_c.shape[:2]
    scale = min((size - 2 * pad) / float(cw), (size - 2 * pad) / float(ch))
    nw = max(1, int(round(cw * scale)))
    nh = max(1, int(round(ch * scale)))

    rgb_up = cv2.resize(rgb_c, (nw, nh), interpolation=cv2.INTER_LANCZOS4)
    a_up = cv2.resize(a_c, (nw, nh), interpolation=cv2.INTER_LANCZOS4)
    if cw < 180:
        blur = cv2.GaussianBlur(rgb_up, (0, 0), 0.9)
        rgb_up = cv2.addWeighted(rgb_up, 1.28, blur, -0.28, 0)

    canvas = np.zeros((size, size, 4), dtype=np.uint8)
    dx = (size - nw) // 2
    dy = (size - nh) // 2
    canvas[dy:dy + nh, dx:dx + nw, :3] = rgb_up
    canvas[dy:dy + nh, dx:dx + nw, 3] = a_up
    return Image.fromarray(canvas, mode="RGBA")


def save_dual_tone_contact_sheet(rgba_img, sheet_path: pathlib.Path, sheet_h: int = 640) -> None:
    """Composite cutout onto a studio (#ECECEA) + mid-slate (#828891) band canvas to expose halos/artifacts."""
    import numpy as np
    from PIL import Image

    ratio = (sheet_h - 40) / float(max(1, rgba_img.height))
    tw = max(1, int(round(rgba_img.width * ratio)))
    thumb = rgba_img.resize((tw, sheet_h - 40), Image.Resampling.LANCZOS)

    canvas_w = tw + 64
    sheet = Image.new("RGB", (canvas_w, sheet_h), (236, 236, 234))
    arr = np.array(sheet)
    arr[int(sheet_h * 0.20):int(sheet_h * 0.78), :, :] = (130, 136, 145)
    sheet = Image.fromarray(arr)
    sheet.paste(thumb, (32, 20), thumb)
    sheet_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(sheet_path, "PNG")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Extract neural studio cutouts (rembg + distance_transform_edt de-haloing) with optional dual-tone contact sheet."
    )
    parser.add_argument("input", type=pathlib.Path, help="Source image path (photo or foreground-sharp frame)")
    parser.add_argument("output", type=pathlib.Path, help="Destination RGBA PNG cutout path")
    parser.add_argument(
        "--mode",
        choices=("model", "packshot", "white-garment"),
        default="model",
        help="Segmentation profile: model (full-body subject), white-garment (white tee + dark denim), packshot (product flat-lay/shoe)",
    )
    parser.add_argument("--target-height", type=int, default=1100, help="Target height for model/white-garment cutouts (default: 1100)")
    parser.add_argument("--target-size", type=int, default=320, help="Square size for packshot cutouts (default: 320)")
    parser.add_argument("--pad", type=int, default=12, help="Outer transparent padding in pixels (default: 12)")
    parser.add_argument("--crop", type=str, default=None, help="Optional fractional crop box x1,y1,x2,y2 (each 0.0-1.0)")
    parser.add_argument("--clean-leg-floor", action="store_true", help="Suppress neutral studio floor captured between ankles (model mode)")
    parser.add_argument("--fill-holes", action="store_true", help="Morphological hole fill for white-upper footwear on light studio cards")
    parser.add_argument("--symmetrize-x", action="store_true", help="Mirror left silhouette onto right side to drop badge corners on symmetrical flat-lays")
    parser.add_argument("--use-u2net", action="store_true", help="Use u2net instead of isnet-general-use for low-contrast light apparel packshots")
    parser.add_argument("--contact-sheet", type=pathlib.Path, default=None, help="Optional dual-tone verification contact-sheet PNG path")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    crop_box = parse_crop(args.crop)
    if not args.input.exists():
        print(f"Error: Input file not found: {args.input}", file=sys.stderr)
        return 1

    try:
        from PIL import Image
    except ImportError as exc:
        print(
            f"Missing runtime dependencies ({exc}). Run with:\n"
            "uv run --with pillow --with numpy --with opencv-python-headless "
            "--with rembg --with onnxruntime --with scipy python scripts/extract_studio_cutout.py ...",
            file=sys.stderr,
        )
        return 1

    src = Image.open(args.input).convert("RGB")
    if crop_box is not None:
        src = crop_fractional(src, crop_box)

    if args.mode == "packshot":
        out_img = extract_packshot_cutout(
            src,
            size=args.target_size,
            pad=args.pad if args.pad != 12 else 18,
            fill_holes=args.fill_holes,
            symmetrize_x=args.symmetrize_x,
            use_u2net=args.use_u2net,
        )
    else:
        out_img = extract_model_cutout(
            src,
            mode=args.mode,
            target_h=args.target_height,
            pad=args.pad,
            clean_leg_floor=args.clean_leg_floor,
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    out_img.save(args.output, "PNG")
    print(f"Saved cutout: {args.output} ({out_img.size})")

    if args.contact_sheet is not None:
        save_dual_tone_contact_sheet(out_img, args.contact_sheet)
        print(f"Saved contact sheet: {args.contact_sheet}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
