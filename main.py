from core.color_matcher import find_closest_bead_color


def main():
    print("=== Bead Color Matcher ===")

    test_colors = [
        (250, 240, 210),
        (255, 255, 255),
        (0, 0, 0),
        (230, 60, 60),
    ]

    for rgb in test_colors:
        code, bead_rgb = find_closest_bead_color(rgb)

        print(f"Input: {rgb}")
        print(f"Closest bead: {code} {bead_rgb}")
        print()


if __name__ == "__main__":
    main()