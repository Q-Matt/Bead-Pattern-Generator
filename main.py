import os
import tkinter as tk
from tkinter import filedialog

from core.image_processor import (
    load_image,
    check_board_size,
    place_on_board,
    resize_to_fit
)
from core.pattern_generator import (
    generate_pattern,
    draw_pattern
)


def main():
    print("=== Bead Pattern Generator ===")

    # Hide the main Tkinter window.
    root = tk.Tk()
    root.withdraw()

    # Ask the user to select an image.
    image_path = filedialog.askopenfilename(
        title="Select an image",
        filetypes=[
            ("Image files", "*.png *.jpg *.jpeg"),
            ("PNG files", "*.png"),
            ("JPEG files", "*.jpg *.jpeg")
        ]
    )

    root.destroy()

    if not image_path:
        print("No image selected.")
        return

    # Load the selected image.
    image = load_image(image_path)

    print("Selected image:", image_path)
    print("Original image size:", image.size)

    # Select board size.
    while True:
        print("\nChoose a board size:")
        print("1. 30 x 30")
        print("2. 60 x 60")
        print("3. 90 x 90")

        choice = input("Enter your choice (1/2/3): ")

        board_sizes = {
            "1": 30,
            "2": 60,
            "3": 90
        }

        if choice in board_sizes:
            board_size = board_sizes[choice]
            break

        print("Invalid choice. Please enter 1, 2, or 3.")

    # Check whether the image fits.
    if not check_board_size(image, board_size):
        print(
            f"Image is too large for a "
            f"{board_size}x{board_size} board."
        )

        answer = input(
            "Would you like to resize it? (y/n): "
        ).strip().lower()

        if answer == "y":
            image = resize_to_fit(image, board_size)
            print("Resized image size:", image.size)
        else:
            print("Image processing cancelled.")
            return

    # Center the image on the board.
    board = place_on_board(image, board_size)

    # Generate pattern using Lab color matching.
    lab_pattern, lab_counts = generate_pattern(
        board, method="lab"
    )

    # Create output directory.
    os.makedirs("output", exist_ok=True)

    # Ask the user to enter an output filename.
    while True:
        filename = input(
            "\nEnter output filename (without .png): "
        ).strip()

        # Check for an empty filename.
        if not filename:
            print("Filename cannot be empty.")
            continue

        # Check for invalid characters.
        if filename in (".", "..") or any(
            char in filename for char in '/\\:'
        ):
            print("Invalid filename. Please try again.")
            continue

        # Generate output file paths.
        lab_path = os.path.join(
            "output", f"{filename}_lab.png"
        )

        # Check whether either file already exists.
        if os.path.exists(lab_path):
            print(f"\nFiles already exist for '{filename}'.")

            while True:
                answer = input(
                    "Would you like to overwrite them? (y/n): "
                ).strip().lower()

                if answer in ("y", "n"):
                    break

                print("Invalid choice. Please enter y or n.")

            if answer == "n":
                print("Please choose a different filename.")
                continue

        # Filename is accepted.
        break

    # Generate output file paths using the user's filename.
    rgb_path = os.path.join(
        "output", f"{filename}_rgb.png"
    )

    lab_path = os.path.join(
        "output", f"{filename}_lab.png"
    )

    # Save Lab pattern.
    lab_image = draw_pattern(lab_pattern, cell_size=30)
    lab_image.save(lab_path)

    print("\n=== Lab Matching ===")
    print("Total Beads:", sum(lab_counts.values()))
    print("Colors Used:", len(lab_counts))

    print("\nSaved:", lab_path)


if __name__ == "__main__":
    main()