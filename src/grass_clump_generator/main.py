from importlib import reload

from .ui import ui_manager
from .utils import modules, paths
from .clump_generator import GrassClumpGenerator
from .data import persistent_settings as ps
from .rendering import render, camera

_ui_manager = ui_manager.UI_Manager()


## callbacks
def tool_loaded():
    print("PyMEL succesfully loaded")
    _ui_manager.create_main_ui()


def generate_clump():
    ## Create clump generator object
    import pymel.core as pm

    print("Generating Clump Mesh...")
    clump_generator = GrassClumpGenerator(
        total_foliage_count=ps.read_value(ps.HEADER_UI_VALUES, "total_foliage_meshes"),
        distribution_radius=float(ps.read_value(ps.HEADER_UI_VALUES, "radius")),
        rotation_variation=float(
            ps.read_value(ps.HEADER_UI_VALUES, "rotation_variation")
        ),
        scale_variation=float(ps.read_value(ps.HEADER_UI_VALUES, "scale_variation")),
        scale_distance=float(ps.read_value(ps.HEADER_UI_VALUES, "scale_by_radius")),
    )
    clump_mesh = clump_generator.generate()
    if clump_mesh:
        print("Generate Clump Mesh Successful")
    else:
        raise Exception("Failed to generate Clump Mesh")

    # -- Render billboard --
    # check if render setting enabled and exit if not.
    if not ps.read_value(ps.HEADER_UI_VALUES, "render_enabled"):
        return True

    # init params
    render_out_name = ps.read_value(ps.HEADER_UI_VALUES, "export_name")
    render_res = [
        int(ps.read_value(ps.HEADER_UI_VALUES, "res_width")),
        int(ps.read_value(ps.HEADER_UI_VALUES, "res_height")),
    ]

    # create billboard cameras
    camera_render = camera.BillboardCameras()
    camera_render.generate()
    cameras = camera_render.get_cameras()

    print("Configuring Render Settings...")
    # configure render settings
    if not render.prerender_settings(
        camera_name=camera_render.get_cameras()[0][0].name(),
        output_dir=paths.get_maya_images_dir(),
        image_base_name=render_out_name,
        image_format="exr",
        width=render_res[0],
        height=render_res[1],
    ):
        raise Exception("Configure Render settings failed")
    print("Configure Render Settings Successful")
    # adjust camera fit with resolution
    camera_render.fit_to_target(clump_mesh, render_res[0], render_res[1])

    print("Rendering Textures...")
    pm.arnoldRender(camera=cameras[0][0].name())


def start():
    """Called on startup"""
    import grass_clump_generator.utils.modules

    reload(grass_clump_generator.utils.modules)
    modules.reimport_modules(grass_clump_generator)
    _ui_manager.create_loading_ui()
