from data.bead_colors import bead_colors


def color_distance(color1, color2):
    r1, g1, b1 = color1
    r2, g2, b2 = color2

    return (
        (r1 - r2) ** 2
        + (g1 - g2) ** 2
        + (b1 - b2) ** 2
    )


def find_closest_bead_color(rgb):
    closest_code = None
    closest_rgb = None
    minimum_distance = float("inf")

    for code, bead_rgb in bead_colors.items():
        distance = color_distance(rgb, bead_rgb)

        if distance < minimum_distance:
            minimum_distance = distance
            closest_code = code
            closest_rgb = bead_rgb

    return closest_code, closest_rgb