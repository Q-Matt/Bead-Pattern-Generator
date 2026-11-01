from PIL import Image, ImageDraw, ImageFont
from data.bead_colors import bead_colors
from collections import Counter

from core.color_matcher import (
    find_closest_bead_color,
    find_closest_bead_color_lab
)


def generate_pattern(image, method="rgb"):
    """
    Convert an RGBA image into a bead pattern.

    method:
        "rgb" - RGB color matching
        "lab" - Lab color matching
    """
    if method == "rgb":
        matcher = find_closest_bead_color
    elif method == "lab":
        matcher = find_closest_bead_color_lab
    else:
        raise ValueError("Invalid color matching method.")

    pattern = []
    bead_counts = Counter()

    for y in range(image.height):
        row = []

        for x in range(image.width):
            r, g, b, a = image.getpixel((x, y))

            if a == 0:
                row.append(None)
                continue

            code, bead_rgb = matcher((r, g, b))

            row.append(code)
            bead_counts[code] += 1

        pattern.append(row)

    return pattern, dict(bead_counts)


def draw_pattern(pattern, cell_size=30):
    """
    Draw a bead pattern as a PNG-compatible image.
    """
    rows = len(pattern)
    cols = len(pattern[0])

    width = cols * cell_size
    height = rows * cell_size

    canvas = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(canvas)

    font = ImageFont.load_default(size=12)

    for y, row in enumerate(pattern):
        for x, code in enumerate(row):
            x1 = x * cell_size
            y1 = y * cell_size
            x2 = x1 + cell_size
            y2 = y1 + cell_size

            if code is None:
                fill_color = (235, 235, 235)
            else:
                fill_color = bead_colors[code]

            draw.rectangle(
                (x1, y1, x2 - 1, y2 - 1),
                fill=fill_color,
                outline=(180, 180, 180)
            )

            if code is not None:
                r, g, b = fill_color
                brightness = (r * 299 + g * 587 + b * 114) / 1000
                text_color = "black" if brightness > 140 else "white"

                draw.text(
                    (x1 + cell_size / 2, y1 + cell_size / 2),
                    code,
                    fill=text_color,
                    font=font,
                    anchor="mm"
                )

    return canvas