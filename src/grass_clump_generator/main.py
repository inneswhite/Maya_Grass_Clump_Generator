from importlib import reload

from .ui import ui_manager
from .utils import modules
from .clump_generator import GrassClumpGenerator
from .data import persistent_settings as ps

_ui_manager = ui_manager.UI_Manager()


## callbacks
def tool_loaded():
    print("PyMEL succesfully loaded")
    _ui_manager.create_main_ui()


def generate_clump():
    ## Create clump generator object

    clump_generator = GrassClumpGenerator(
        total_foliage_count=ps.read_value(ps.HEADER_UI_VALUES, "total_foliage_meshes"),
        distribution_radius=float(ps.read_value(ps.HEADER_UI_VALUES, "radius")),
        rotation_variation=float(
            ps.read_value(ps.HEADER_UI_VALUES, "rotation_variation")
        ),
        scale_variation=float(ps.read_value(ps.HEADER_UI_VALUES, "scale_variation")),
        scale_distance=float(ps.read_value(ps.HEADER_UI_VALUES, "scale_by_radius")),
        render_billboards=ps.read_value(ps.HEADER_UI_VALUES, "render_enabled"),
        render_name=ps.read_value(ps.HEADER_UI_VALUES, "export_name"),
        render_resolution=[
            int(ps.read_value(ps.HEADER_UI_VALUES, "res_width")),
            int(ps.read_value(ps.HEADER_UI_VALUES, "res_height")),
        ],
    )
    clump_generator.generate()


def start():
    """Called on startup"""
    import grass_clump_generator.utils.modules

    reload(grass_clump_generator.utils.modules)
    modules.reimport_modules(grass_clump_generator)
    _ui_manager.create_loading_ui()
