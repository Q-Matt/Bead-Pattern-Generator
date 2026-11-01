
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from core.image_processor import (
    load_image,
    check_board_size,
    resize_to_fit,
    place_on_board
)

from core.pattern_generator import (
    generate_pattern,
    draw_pattern
)


class BeadPatternGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Bead Pattern Generator")
        self.root.geometry("650x600")
        self.root.minsize(550, 500)

        # Store user selections.
        self.image_path = None
        self.board_size = tk.StringVar(value="30")
        self.save_directory = tk.StringVar(
            value=os.path.abspath("output")
        )

        # Main container.
        main_frame = ttk.Frame(root, padding=20)
        main_frame.pack(fill="both", expand=True)

        # Title.
        title_label = ttk.Label(
            main_frame,
            text="Bead Pattern Generator",
            font=("Arial", 20, "bold")
        )
        title_label.pack(pady=(0, 20))

        # Image selection.
        image_frame = ttk.LabelFrame(
            main_frame,
            text="1. Select Image",
            padding=15
        )
        image_frame.pack(fill="x", pady=10)

        self.image_label = ttk.Label(
            image_frame,
            text="No image selected"
        )
        self.image_label.pack(pady=5)

        select_button = ttk.Button(
            image_frame,
            text="Browse Image",
            command=self.select_image
        )
        select_button.pack(pady=5)

        # Board size selection.
        board_frame = ttk.LabelFrame(
            main_frame,
            text="2. Board Size",
            padding=15
        )
        board_frame.pack(fill="x", pady=10)

        for size in (30, 60, 90):
            radio = ttk.Radiobutton(
                board_frame,
                text=f"{size} x {size}",
                variable=self.board_size,
                value=str(size)
            )
            radio.pack(side="left", padx=15)

        # Output filename.
        filename_frame = ttk.LabelFrame(
            main_frame,
            text="3. Output Filename",
            padding=15
        )
        filename_frame.pack(fill="x", pady=10)

        self.filename_entry = ttk.Entry(filename_frame)
        self.filename_entry.insert(0, "my_bead_pattern")
        self.filename_entry.pack(fill="x")

        # Save location selection.
        save_frame = ttk.LabelFrame(
            main_frame,
            text="4. Save Location",
            padding=15
        )
        save_frame.pack(fill="x", pady=10)

        self.save_location_entry = ttk.Entry(
            save_frame,
            textvariable=self.save_directory,
            state="readonly"
        )
        self.save_location_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 10)
        )

        browse_save_button = ttk.Button(
            save_frame,
            text="Browse",
            command=self.select_save_directory
        )
        browse_save_button.pack(side="right")

        # Generate Lab Pattern button
        generate_button = ttk.Button(
            main_frame,
            text="Generate Lab Pattern",
            command=self.generate
        )
        generate_button.pack(pady=20)

        # Status label
        self.status_label = ttk.Label(
            main_frame,
            text="Ready to generate"
        )
        self.status_label.pack(pady=5)

    def select_save_directory(self):
        directory = filedialog.askdirectory(
            title="Select Save Location",
            initialdir=self.save_directory.get()
        )

        if directory:
            self.save_directory.set(directory)
    
    def select_image(self):
        image_path = filedialog.askopenfilename(
            title="Select an image",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg"),
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg *.jpeg")
            ]
        )

        if image_path:
            self.image_path = image_path
            self.image_label.config(
                text=image_path.split("/")[-1]
            )

    
    def generate(self):
        # 1. Check whether an image has been selected.
        if not self.image_path:
            messagebox.showerror(
                "Error",
                "Please select an image first."
            )
            return

        # 2. Validate the output filename.
        filename = self.filename_entry.get().strip()

        if not filename:
            messagebox.showerror(
                "Error",
                "Output filename cannot be empty."
            )
            return

        if filename in (".", "..") or any(
            char in filename for char in '/\\:'
        ):
            messagebox.showerror(
                "Error",
                "The filename contains invalid characters."
            )
            return

        # 3. Get the selected board size.
        board_size = int(self.board_size.get())

        try:
            # 4. Load the selected image.
            image = load_image(self.image_path)

            # 5. Ask before resizing a large image.
            if not check_board_size(image, board_size):
                answer = messagebox.askyesno(
                    "Resize Image",
                    f"The image is larger than "
                    f"{board_size} x {board_size}.\n\n"
                    "Would you like to resize it?"
                )

                if not answer:
                    self.status_label.config(
                        text="Generation cancelled."
                    )
                    return

                image = resize_to_fit(image, board_size)

            # 6. Center the image on the board.
            board = place_on_board(image, board_size)

            # 7. Generate the Lab pattern.
            pattern, bead_counts = generate_pattern(
                board,
                method="lab"
            )

            # 8. Draw the numbered pattern.
            result_image = draw_pattern(
                pattern,
                cell_size=30
            )

            # 9. Prepare the output path.
            save_directory = self.save_directory.get()

            os.makedirs(save_directory, exist_ok=True)

            output_path = os.path.join(
                save_directory,
                f"{filename}_lab.png"
            )

            # 10. Confirm before overwriting a file.
            if os.path.exists(output_path):
                answer = messagebox.askyesno(
                    "Overwrite File",
                    f"{filename}_lab.png already exists.\n\n"
                    "Would you like to overwrite it?"
                )

                if not answer:
                    self.status_label.config(
                        text="Generation cancelled."
                    )
                    return

            # 11. Save the pattern.
            result_image.save(output_path)

            # 12. Update the status.
            total_beads = sum(bead_counts.values())
            colors_used = len(bead_counts)

            self.status_label.config(
                text=(
                    f"Done! {total_beads} beads, "
                    f"{colors_used} colors."
                )
            )

            messagebox.showinfo(
                "Success",
                f"Lab pattern generated successfully!\n\n"
                f"Total beads: {total_beads}\n"
                f"Colors used: {colors_used}\n\n"
                f"Saved to: {os.path.abspath(output_path)}"
            )

        except Exception as error:
            self.status_label.config(
                text="Generation failed."
            )

            messagebox.showerror(
                "Generation Error",
                str(error)
            )

if __name__ == "__main__":
    root = tk.Tk()
    app = BeadPatternGUI(root)
    root.mainloop()
