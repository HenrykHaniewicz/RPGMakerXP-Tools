import sys
import os
from PIL import Image

def scale_and_trim_tiles(input_path, output_path):
    """Resize a 256x256 tile sheet and trim each tile to 32x48, saving the result.

    The input image is expected to be 256x256 pixels, containing a 4x4 grid of 64x64 tiles.
    Each tile is scaled to 48x48 (75%) and then trimmed horizontally to 32x48 by removing 8 pixels
    from both sides. The resulting image (128x192) is saved to the specified output path.

    Args:
        input_path (str): Path to the input 256x256 image.
        output_path (str): Path where the processed image will be saved.
    
    Raises:
        ValueError: If the input image is not 256x256 pixels.
    """
    original_tile_size = 64
    scaled_tile_size = 48
    trimmed_tile_width = 32
    tile_height = 48
    grid_size = 4

    img = Image.open(input_path)

    if img.size != (256, 256):
        raise ValueError("Expected 256x256 input image.")

    # Resize image by 0.75 → 192x192
    scaled_img = img.resize((192, 192), Image.LANCZOS)

    # Create output image (128x192)
    output_img = Image.new("RGBA", (grid_size * trimmed_tile_width, grid_size * tile_height))

    for y in range(grid_size):
        for x in range(grid_size):
            left = x * scaled_tile_size
            top = y * tile_height
            tile = scaled_img.crop((left, top, left + scaled_tile_size, top + tile_height))
            tile = tile.crop((8, 0, 40, tile_height))  # Trim 8px from left/right → 32x48
            output_img.paste(tile, (x * trimmed_tile_width, y * tile_height))

    output_img.save(output_path)
    print(f"Saved processed image to {output_path}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 format_gen4_2_gen3.py input_picture1 input_picture2 etc")
        sys.exit(1)
    
    for i, img in enumerate(sys.argv[1:]):
        input_path = os.path.abspath(sys.argv[i + 1])

        if not (input_path.lower().endswith(".png") or input_path.lower().endswith(".jpg")):
            print("Input file must be a .png or .jpg")
            continue

        # Construct output path with _gen3 before .png or .jpg
        base, ext = os.path.splitext(os.path.basename(input_path))
        output_filename = f"{base}_gen3{ext}"
        output_path = os.path.join(os.path.dirname(input_path), output_filename)

        try:
            scale_and_trim_tiles(input_path, output_path)
        except ValueError:
            print(f"scale_and_trim_tiles encountered a ValueError whilst processing {input_path}")
            continue

if __name__ == "__main__":
    main()