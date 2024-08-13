import grass_clump_generator.ui.ui_billboard_settings
import grass_clump_generator.ui.ui_clump_settings
import grass_clump_generator.ui.ui_foliage_distributions
import grass_clump_generator.ui.ui_grass_clump_generator
from grass_clump_generator.ui import ui_manager
import grass_clump_generator.data.persistent_settings
from importlib import reload

import grass_clump_generator.utils
import grass_clump_generator.utils.modules
from .utils import modules, paths
import grass_clump_generator.ui.ui_slider_spinbox
import grass_clump_generator.ui.ui_utils


def reload_pypackages():
    """_summary_"""
    reload(grass_clump_generator.data.persistent_settings)
    reload(grass_clump_generator.ui.ui_slider_spinbox)
    reload(grass_clump_generator.ui.ui_manager)
    reload(grass_clump_generator.ui.ui_grass_clump_generator)
    reload(grass_clump_generator.ui.ui_clump_settings)
    reload(grass_clump_generator.ui.ui_foliage_distributions)
    reload(grass_clump_generator.ui.ui_utils)
    reload(grass_clump_generator.ui.ui_billboard_settings)


_ui_manager = ui_manager.UI_Manager()


## callbacks
def tool_loaded():
    _ui_manager.create_main_ui()


def generate_clump():
    pass


def start():
    """Called on startup"""
    reload(grass_clump_generator.utils.modules)
    modules.reimport_modules(grass_clump_generator)
    _ui_manager.create_loading_ui()
