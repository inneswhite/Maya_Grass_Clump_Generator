import grass_clump_generator.ui.ui_grass_clump_generator as main_ui
import grass_clump_generator.ui.ui_loading as ui_loading
from importlib import reload


class UI_Manager:
    def __init__(self):
        pass

    def create_loading_ui(self):
        reload(ui_loading)
        self.pymel_loading_bar = ui_loading.LoadingBar(
            title="Loading PyMEL", loading_message="Loading PyMEL"
        )
        self.pymel_loading_bar.show()

    def create_main_ui(self):
        reload(main_ui)
        self.main_ui = main_ui.ClumpGeneratorUI()
        self.main_ui.show(dockable=True)
