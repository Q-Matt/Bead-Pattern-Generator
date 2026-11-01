import numpy as np
from skimage.color import rgb2lab
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

def rgb_to_lab(rgb):
    """
    Convert an RGB color to CIELAB.
    """
    rgb_array = np.array(
        [[rgb]],
        dtype=np.float64
    ) / 255.0

    lab_array = rgb2lab(rgb_array)

    return lab_array[0, 0]


# Convert the bead palette only once.
bead_colors_lab = {
    code: rgb_to_lab(rgb)
    for code, rgb in bead_colors.items()
}


def find_closest_bead_color_lab(rgb):
    """
    Find the closest bead color using Lab distance.
    """
    target_lab = rgb_to_lab(rgb)

    closest_code = None
    minimum_distance = float("inf")

    for code, bead_lab in bead_colors_lab.items():
        distance = np.sum(
            (target_lab - bead_lab) ** 2
        )

        if distance < minimum_distance:
            minimum_distance = distance
            closest_code = code

    return closest_code, bead_colors[closest_code]