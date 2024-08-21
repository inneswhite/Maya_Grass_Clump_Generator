from .data import persistent_settings as ps
from .rendering import camera, render
from .utils import paths, image
import os


def render_texture(
    camera_render,
    camera_name,
    temp_render_dir,
    temp_front_base_name,
    render_res,
    clump_mesh,
):
    import pymel.core as pm

    # configure front render settings
    if not render.prerender_settings(
        camera_name=camera_name,
        output_dir=temp_render_dir,
        image_base_name=temp_front_base_name,
        image_format="tif",
        width=render_res[0],
        height=render_res[1],
    ):
        raise Exception("Configure Render settings failed")
    print("Configure Render Settings Successful")
    # adjust camera fit with resolution
    camera_render.fit_to_target(clump_mesh, render_res[0], render_res[1])

    print("Rendering Textures...")
    pm.arnoldRender(camera=camera_name)


def merge_renders(
    temp_render_dir, temp_front_base_name, temp_right_base_name, render_out_name
):
    # get renders
    wildcard_pattern = "*.tif"
    front_render_path = paths.find_matching_files(
        temp_render_dir, temp_front_base_name + wildcard_pattern
    )
    if len(front_render_path) > 1:
        raise Exception(
            f"{len(front_render_path)} files match search query; {temp_render_dir} + {wildcard_pattern}"
        )
    elif not front_render_path:
        raise Exception(f"no matches for file search in {temp_render_dir}")

    right_render_path = paths.find_matching_files(
        temp_render_dir, temp_right_base_name + wildcard_pattern
    )
    if len(right_render_path) > 1:
        raise Exception(
            f"{len(right_render_path)} files match search query; {temp_render_dir} + {wildcard_pattern}"
        )
    elif not right_render_path:
        raise Exception(f"no matches for file search in {temp_render_dir}")

    # merge renders
    front_image = image.get_image(front_render_path[0])
    right_image = image.get_image(right_render_path[0])

    merged_image = image.merge_images_vert(front_image, right_image)
    merged_output_name = os.path.join(
        paths.get_maya_images_dir(), (render_out_name + ".tif")
    )
    merged_image.save(merged_output_name)


def render_clump(clump_mesh, render_normals: bool = False):
    import pymel.core as pm

    # init params
    render_out_name = ps.read_value(ps.HEADER_UI_VALUES, "export_name")
    render_res = [
        int(ps.read_value(ps.HEADER_UI_VALUES, "res_width")),
        int(ps.read_value(ps.HEADER_UI_VALUES, "res_height")),
    ]

    # create billboard cameras
    camera_render = camera.BillboardCameras()
    camera_render.generate()

    print("Configuring Render Settings...")

    temp_render_dir = paths.get_maya_temp_images_dir()
    temp_front_base_name = (
        f"temp_{render_out_name}_{camera_render.get_cameras()[0][0].name()}"
    )
    temp_right_base_name = (
        f"temp_{render_out_name}_{camera_render.get_cameras()[1][0].name()}"
    )

    # render front
    render_texture(
        camera_render,
        camera_render.get_cameras()[0][0].name(),
        temp_render_dir,
        temp_front_base_name,
        render_res,
        clump_mesh,
    )

    # render side
    render_texture(
        camera_render,
        camera_render.get_cameras()[1][0].name(),
        temp_render_dir,
        temp_right_base_name,
        render_res,
        clump_mesh,
    )

    if render_normals:
        render_out_name = render_out_name + "_N"

    merge_renders(
        temp_render_dir, temp_front_base_name, temp_right_base_name, render_out_name
    )
