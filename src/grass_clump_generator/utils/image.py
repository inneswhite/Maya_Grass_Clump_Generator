from PIL import Image
import OpenEXR
import Imath
import numpy
import numexpr as ne
from grass_clump_generator.utils import paths
import os

PIX_FLOAT = Imath.PixelType(Imath.PixelType.FLOAT)


def get_image(path: str) -> Image:
    """Returns an image from an image's path

    Args:
        path (str): the path of the image file

    Returns:
        Image: image from given path
    """
    try:
        image = Image.open(path)
        return image
    except:
        print(f"Could not find image in directory {path}")


def merge_images_vert(image1: Image.Image, image2: Image.Image) -> Image.Image:
    """Creates a single image with image1 taking up the top portion, and image2 underneath it.

    Args:
        image1 (Image): Image to appear on top
        image2_path (Image): Image to appear on bottom

    Returns:
        Image: Merged image
    """
    width = max(image1.size[0], image2.size[0])
    height = image1.size[1] + image2.size[1]

    im = Image.new("RGBA", (width, height))

    im.paste(image1)
    im.paste(image2, (0, image1.size[1]))
    return im


if __name__ == "__main__":
    image_top = get_image(
        r"C:\Users\Innes\Perforce\Unreal_Shaders\Maya\images\tmp\masterLayer\0__cam_Camera_Front_Foliage1_1024x512_frame_1_0001.tif"
    )
    image_bottom = get_image(
        r"C:\Users\Innes\Perforce\Unreal_Shaders\Maya\images\tmp\masterLayer\0__cam_Camera_Right_Foliage1_1024x512_frame_1_0001.tif"
    )

    merged_im = merge_images_vert(image_top, image_bottom)
    output_path = paths.get_maya_images_dir()
    merged_im.save(os.path.join(output_path, "merged.tif"))
