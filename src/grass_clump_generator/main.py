from importlib import reload
import os

from PIL import Image
from .ui import ui_manager
from .utils import modules, paths, image
from .clump_generator import GrassClumpGenerator
from .data import persistent_settings as ps
from .rendering import render, camera, material
from . import clump_renderer

_ui_manager = ui_manager.UI_Manager()


## callbacks
def tool_loaded():
    """Creates the main UI
    Called when pymel loading UI is closed.
    """

    print("PyMEL succesfully loaded")
    _ui_manager.create_main_ui()


def generate_clump():
    """Creates the call to generate the clump mesh and render
    Called when user presses "Generate Clump on UI".
    """
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

    clump_renderer.render_clump(clump_mesh)

    # apply normal material
    pm.sets(material.tan_nrm_mat()[1], forceElement=clump_mesh)

    clump_renderer.render_clump(clump_mesh, render_normals=True)


def start():
    """Called on startup"""
    import pymel.core as pm
    import grass_clump_generator.utils.modules

    reload(grass_clump_generator.utils.modules)
    modules.reimport_modules(grass_clump_generator)

    _ui_manager.create_loading_ui()
