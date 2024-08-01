import grass_clump_generator.ui.ui_manager
from importlib import reload


def run():
    reload(grass_clump_generator.ui.ui_manager)
    grass_clump_generator.ui.ui_manager._ui_manager.create_loading_ui()
