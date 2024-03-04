"""This file is used to draw layouts for Discord thumbnails based on number of usernames"""
import requests
from PIL import Image, ImageDraw
from io import BytesIO


IMAGE_WIDTH = 96
IMAGE_HEIGHT = 96
LINE_WIDTH = 1
LINE_COLOR = 'white'
COMPOSITE_BACKGROUND_COLOR = (0, 0, 0, 0) # Transparent background
IMG_DIR = 'assets/images/'

def calculate_position(index, cols):
    """Calculate the x, y position based on the index."""
    x = (index % cols) * (IMAGE_WIDTH + LINE_WIDTH)
    y = (index // cols) * (IMAGE_HEIGHT + LINE_WIDTH)
    return x, y

def draw_lines(draw, cols, rows, composite_width, composite_height):
    if cols > 1:
        for i in range(1, cols):
            line_x = i * IMAGE_WIDTH + (i - 1) * LINE_WIDTH
            draw.line([(line_x, 0), (line_x, composite_height)], fill=LINE_COLOR, width=LINE_WIDTH)
    if rows > 1:
        for i in range(1, rows):
            line_y = i * IMAGE_HEIGHT + (i - 1) * LINE_WIDTH
            draw.line([(0, line_y), (composite_width, line_y)], fill=LINE_COLOR, width=LINE_WIDTH)

def compose_images(usernames, cols, composite_image):
    """Compose the images on the composite image."""
    for i in range(len(usernames)):
        image_path = f'{IMG_DIR}{i+1}.png'
        image = Image.open(image_path)
        x, y = calculate_position(i, cols)
        composite_image.paste(image, (x, y))

def calculate_composite_dimensions(cols, rows):
    """Calculate the dimensions of the composite image."""
    composite_width = IMAGE_WIDTH * cols + LINE_WIDTH * (cols - 1)
    composite_height = IMAGE_HEIGHT * rows + LINE_WIDTH * (rows - 1)
    return composite_width, composite_height

def get_layout(num_images):
    """Determine the layout based on the number of images."""
    if num_images == 1:
        cols = 1
        rows = 1
    elif num_images == 2:
        cols = 2
        rows = 1
    elif num_images == 3:
        cols = 2  # We'll adjust positioning manually for 3 images
        rows = 2
    elif num_images == 4:
        cols = 2
        rows = 2
    return cols, rows

def compose_triangle_layout(usernames, composite_image, cols, composite_width, draw):
    # Place images 1 and 2 above the bottom image
    for i in range(len(usernames[:-1])):
        image_path = f'{IMG_DIR}{i+1}.png'
        image = Image.open(image_path)
        # Position the images above the bottom image
        x = (i % cols) * (IMAGE_WIDTH + LINE_WIDTH)
        y = 0
        composite_image.paste(image, (x, y))

    # Place image 3 at the bottom-center
        image_path = f'{IMG_DIR}3.png'
        image = Image.open(image_path)
        x = (composite_width - IMAGE_WIDTH) // 2
        y = IMAGE_HEIGHT + LINE_WIDTH
        composite_image.paste(image, (x, y))

    # Draw the T shaped line for triangle layout
    draw.line([(composite_width // 2, 0), (composite_width // 2, IMAGE_HEIGHT)], fill=LINE_COLOR, width=LINE_WIDTH)
    line_y = IMAGE_HEIGHT + LINE_WIDTH // 2
    draw.line([(0, line_y), (composite_width, line_y)], fill=LINE_COLOR, width=LINE_WIDTH)
    

def create_composite_image(usernames):
    num_images = len(usernames)
    cols, rows = get_layout(num_images)

    # Setup composite dimensions
    composite_width, composite_height = calculate_composite_dimensions(cols, rows)

    composite_image = Image.new('RGBA', (composite_width, composite_height), COMPOSITE_BACKGROUND_COLOR)
    
    # Init ImageDraw object for drawing lines later
    draw = ImageDraw.Draw(composite_image)

    # We hardcode 3 here because we want a special layout for 3
    if num_images == 3:
        compose_triangle_layout(usernames, composite_image, cols, composite_width, draw)
    else:
        # For cases 1,2,4
        compose_images(usernames, cols, composite_image)
        draw_lines(draw, cols, rows, composite_width, composite_height)

    img_dir = 'assets/images/'
    composite_image_path = f'{img_dir}composite_image.png'
    composite_image.save(composite_image_path)
    return composite_image_path


"""Saving images from a url logic here"""
def save_image_from_url(image_url, save_path):
    response = requests.get(image_url)

    response.raise_for_status() # Raise an exception if request was unsuccessful

    image = Image.open(BytesIO(response.content))

    image.save(save_path)