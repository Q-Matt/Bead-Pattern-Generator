from PIL import Image

def load_image(image_path):
    """Load an image and preserve transparency."""
    image = Image.open(image_path)
    return image.convert("RGBA")


def get_image_size(image):
    """Return the original image dimensions."""
    return image.size


def check_board_size(image, board_size):
    """Check whether an image fits on the selected board."""
    width, height = image.size

    return width <= board_size and height <= board_size


def place_on_board(image, board_size):
    """Center an image without resizing it."""
    if not check_board_size(image, board_size):
        raise ValueError("Image is larger than the selected board.")

    board = Image.new(
        "RGBA",
        (board_size, board_size),
        (0, 0, 0, 0)
    )

    x = (board_size - image.width) // 2
    y = (board_size - image.height) // 2

    board.paste(image, (x, y))

    return board

def resize_to_fit(image, board_size):
    """
    Resize an image to fit within a square board
    while preserving its aspect ratio.
    """
    width, height = image.size

    scale = min(
        board_size / width,
        board_size / height
    )

    new_width = max(1, round(width * scale))
    new_height = max(1, round(height * scale))

    resized_image = image.resize(
        (new_width, new_height),
        Image.Resampling.NEAREST
    )

    return resized_image
