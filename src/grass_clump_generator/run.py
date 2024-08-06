import grass_clump_generator.ui.ui_clump_settings
import grass_clump_generator.ui.ui_foliage_distributions
import grass_clump_generator.ui.ui_grass_clump_generator
import grass_clump_generator.ui.ui_manager
import grass_clump_generator.data.persistent_settings
from importlib import reload

import grass_clump_generator.ui.ui_slider_spinbox
import grass_clump_generator.ui.ui_utils


def reload_pypackages():
    reload(grass_clump_generator.data.persistent_settings)
    reload(grass_clump_generator.ui.ui_slider_spinbox)
    reload(grass_clump_generator.ui.ui_manager)
    reload(grass_clump_generator.ui.ui_grass_clump_generator)
    reload(grass_clump_generator.ui.ui_clump_settings)
    reload(grass_clump_generator.ui.ui_foliage_distributions)
    reload(grass_clump_generator.ui.ui_utils)


def run():
    reload_pypackages()
    grass_clump_generator.ui.ui_manager._ui_manager.create_loading_ui()
