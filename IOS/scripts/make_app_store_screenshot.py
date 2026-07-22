#!/usr/bin/env python3
"""Compose an App Store marketing screenshot with headline + app capture."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageFilter

CANVAS_W = 1290
CANVAS_H = 2796

ROAD_NAVY = (28, 51, 87)
HIGHWAY_TEAL = (41, 112, 128)
BG_BOTTOM = (131, 168, 173)  # matched to 01-signs-example.png
TEXT_SECONDARY = (210, 220, 230)
WARM_CREAM = (247, 242, 232)
LIGHT_BLUE = (239, 244, 249)
SIGNAL_AMBER = (245, 166, 36)
WHITE = (255, 255, 255)


def load_font(size: int, bold: bool = False, rounded: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    if rounded:
        candidates = [
            "/System/Library/Fonts/SFNSRounded.ttf",
            "/System/Library/Fonts/Supplemental/Avenir Next.ttc",
        ]
    else:
        candidates = [
            "/System/Library/Fonts/Supplemental/Avenir Next.ttc",
            "/System/Library/Fonts/SFNS.ttf",
            "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        ]
    for path in candidates:
        if not Path(path).exists():
            continue
        try:
            if path.endswith(".ttc"):
                # Avenir Next: 0=Regular, 2=Medium, 8=Bold, 10=Heavy
                index = 8 if bold else 2
                return ImageFont.truetype(path, size=size, index=index)
            return ImageFont.truetype(path, size=size)
        except OSError:
            continue
    return ImageFont.load_default()


def app_store_background(size: tuple[int, int]) -> Image.Image:
    """Vertical gradient like docs/app-store-screenshots/01-signs-example.png."""
    w, h = size
    strip = Image.new("RGB", (1, h))
    px = strip.load()
    for y in range(h):
        t = y / max(h - 1, 1)
        color = tuple(
            int(ROAD_NAVY[i] * (1 - t) + BG_BOTTOM[i] * t) for i in range(3)
        )
        px[0, y] = color
    return strip.resize((w, h), Image.Resampling.BILINEAR)


def light_background(size: tuple[int, int]) -> Image.Image:
    """Legacy cream gradient — prefer app_store_background()."""
    return app_store_background(size)


def rounded_mask(size: tuple[int, int], radius: int) -> Image.Image:
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([(0, 0), size], radius=radius, fill=255)
    return mask


def wrap_text(text: str, font: ImageFont.ImageFont, max_width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        trial = f"{current} {word}".strip()
        if font.getlength(trial) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_centered_lines(
    draw: ImageDraw.ImageDraw,
    lines: list[str],
    y_start: int,
    font: ImageFont.ImageFont,
    fill: tuple[int, int, int],
    line_gap: int,
    canvas_w: int = CANVAS_W,
) -> int:
    y = y_start
    for line in lines:
        w = font.getlength(line)
        x = (canvas_w - w) // 2
        draw.text((x, y), line, font=font, fill=fill)
        y += line_gap
    return y


def compose(
    screenshot: Path,
    output: Path,
    headline: str,
    subtitle: str = "",
    badge: str = "",
    canvas_w: int = CANVAS_W,
    canvas_h: int = CANVAS_H,
) -> None:
    canvas = app_store_background((canvas_w, canvas_h))
    draw = ImageDraw.Draw(canvas)

    scale = canvas_w / CANVAS_W
    title_font = load_font(int(86 * scale), bold=True, rounded=True)
    subtitle_font = load_font(int(44 * scale), bold=False, rounded=True)

    margin_x = int(88 * scale)
    max_text_w = canvas_w - margin_x * 2

    title_y = int(148 * scale)
    if badge.strip():
        badge_font = load_font(int(34 * scale), bold=True, rounded=True)
        badge_w = badge_font.getlength(badge) + int(56 * scale)
        badge_h = int(58 * scale)
        badge_x = (canvas_w - badge_w) // 2
        badge_y = int(148 * scale)
        draw.rounded_rectangle(
            [(badge_x, badge_y), (badge_x + badge_w, badge_y + badge_h)],
            radius=badge_h // 2,
            fill=HIGHWAY_TEAL,
        )
        draw.text(
            (badge_x + int(28 * scale), badge_y + int(10 * scale)),
            badge,
            font=badge_font,
            fill=WHITE,
        )
        title_y = int(260 * scale)

    title_lines = wrap_text(headline, title_font, max_text_w)
    subtitle_lines = wrap_text(subtitle, subtitle_font, max_text_w) if subtitle.strip() else []

    y = draw_centered_lines(draw, title_lines, title_y, title_font, WHITE, int(98 * scale), canvas_w)
    if subtitle_lines:
        y += int(20 * scale)
        y = draw_centered_lines(
            draw, subtitle_lines, y, subtitle_font, TEXT_SECONDARY, int(56 * scale), canvas_w
        )

    # Amber accent line (like reference example)
    line_w = int(min(max(title_font.getlength(l) for l in title_lines) * 0.42, 180 * scale))
    line_x = (canvas_w - line_w) // 2
    line_y = y + int(18 * scale)
    draw.rounded_rectangle(
        [(line_x, line_y), (line_x + line_w, line_y + max(4, int(5 * scale)))],
        radius=3,
        fill=SIGNAL_AMBER,
    )

    shot = Image.open(screenshot).convert("RGBA")
    phone_w = int(980 * scale)
    phone_scale = phone_w / shot.width
    phone_h = int(shot.height * phone_scale)
    shot = shot.resize((phone_w, phone_h), Image.Resampling.LANCZOS)

    radius = int(52 * scale)
    mask = rounded_mask((phone_w, phone_h), radius)
    phone_layer = Image.new("RGBA", (phone_w, phone_h), (0, 0, 0, 0))
    phone_layer.paste(shot, (0, 0), mask)

    pad = int(50 * scale)
    shadow = Image.new("RGBA", (phone_w + pad * 2, phone_h + pad * 2), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    shadow_draw.rounded_rectangle(
        [(pad, pad), (phone_w + pad, phone_h + pad)],
        radius=radius,
        fill=(ROAD_NAVY[0], ROAD_NAVY[1], ROAD_NAVY[2], 45),
    )
    shadow = shadow.filter(ImageFilter.GaussianBlur(int(28 * scale)))

    phone_x = (canvas_w - phone_w) // 2
    phone_y = canvas_h - phone_h - int(48 * scale)

    canvas_rgba = canvas.convert("RGBA")
    canvas_rgba.alpha_composite(shadow, (phone_x - pad, phone_y - int(30 * scale)))
    canvas_rgba.alpha_composite(phone_layer, (phone_x, phone_y))

    border = ImageDraw.Draw(canvas_rgba)
    border.rounded_rectangle(
        [(phone_x, phone_y), (phone_x + phone_w, phone_y + phone_h)],
        radius=radius,
        outline=(ROAD_NAVY[0], ROAD_NAVY[1], ROAD_NAVY[2], 35),
        width=max(1, int(2 * scale)),
    )

    output.parent.mkdir(parents=True, exist_ok=True)
    canvas_rgba.convert("RGB").save(output, format="PNG", compress_level=6)
    print(f"Saved: {output} ({canvas_w}x{canvas_h})")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("screenshot", type=Path)
    parser.add_argument("-o", "--output", type=Path, required=True)
    parser.add_argument("--headline", required=True)
    parser.add_argument("--subtitle", default="")
    parser.add_argument("--badge", default="")
    args = parser.parse_args()
    compose(args.screenshot, args.output, args.headline, args.subtitle, args.badge)


if __name__ == "__main__":
    main()
