import grass_clump_generator.ui.ui_grass_clump_generator as ui
from importlib import reload


def run():
    reload(ui)
    ui.create_ui()
