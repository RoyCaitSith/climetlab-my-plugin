import math
from PIL import Image as PILImage

def combine_images_grid(image_files, output_file, columns=3, padding=0):

    images = [PILImage.open(image_file) for image_file in image_files]

    max_width = max(image.width for image in images)
    max_height = max(image.height for image in images)

    rows = math.ceil(len(images)/columns)
    grid_size = rows * columns

    # Fill the remaining spots with white images
    if len(images) < grid_size:
        white_image = PILImage.new('RGB', (max_width, max_height), (255, 255, 255))
        for _ in range(grid_size - len(images)):
            images.append(white_image)

    total_width = max_width * columns + padding * (columns - 1)
    total_height = max_height * rows + padding * (rows - 1)

    combined_image = PILImage.new('RGB', (total_width, total_height))

    for i, image in enumerate(images):
        x = i % columns
        y = i // columns

        x_offset = x * (max_width + padding)
        y_offset = y * (max_height + padding)

        combined_image.paste(image, (x_offset, y_offset))

    combined_image.save(output_file)
