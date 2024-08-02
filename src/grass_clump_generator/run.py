import grass_clump_generator.ui.ui_manager
import grass_clump_generator.data.persitent_settings
from importlib import reload

import grass_clump_generator.ui.ui_slider_spinbox

def reload_pypackages():
    reload(grass_clump_generator.data.persitent_settings)
    reload(grass_clump_generator.ui.ui_slider_spinbox)
    reload(grass_clump_generator.ui.ui_manager)

def run():
    reload_pypackages()
    grass_clump_generator.ui.ui_manager._ui_manager.create_loading_ui()

