from PySide2.QtWidgets import *
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
from grass_clump_generator.ui import ui_utils
from grass_clump_generator import main
from grass_clump_generator.data import persistent_settings as ps

# UI Class Imports
from grass_clump_generator.ui.ui_foliage_distributions import FoliageDistributionsUI
from grass_clump_generator.ui.ui_clump_settings import ClumpGenerationSettingsUI
from grass_clump_generator.ui.ui_slider_spinbox import SliderSpinBox
from grass_clump_generator.ui.ui_billboard_settings import BillboardSettings


class ClumpGeneratorUI(MayaQWidgetDockableMixin, QDialog):
    def __init__(self, parent=ui_utils.maya_main_window()):
        super(ClumpGeneratorUI, self).__init__(parent)

        self.setWindowTitle("Grass Clump Generator")
        self.setGeometry(100, 100, 300, 200)

        self.btn_select_foliage = QPushButton("Get Foliage From Selection")
        self.btn_select_foliage.clicked.connect(self.create_ui)

        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.btn_select_foliage)

        self.setLayout(self.main_layout)

    ## Listeners
    def create_ui(self):
        """Generates the main UI elements for the tool.
        Called after Get Foliage from Selection is pressed
        """
        import pymel.core as pm

        self.btn_select_foliage.setHidden(True)

        # Write fresh selection values to .ini
        ps.clear_section(ps.HEADER_SOURCE_MESHES)
        for index, obj in enumerate(pm.selected()):
            if obj.name():
                ps.write_value(
                    ps.HEADER_SOURCE_MESHES, f"source_mesh_{index}", obj.name()
                )
        self.foliage_src = pm.selected()

        # Generate the foliage distributions settins setting
        gbox_foliage_distributions = QGroupBox("Foliage Distributions")
        self.foliage_distribution_ui = FoliageDistributionsUI(self.foliage_src)
        gbox_foliage_distributions.setLayout(self.foliage_distribution_ui.layout)
        self.main_layout.addWidget(gbox_foliage_distributions)

        self.clump_generation_settings_ui = ClumpGenerationSettingsUI()
        gbox_clump_generation_settings = QGroupBox("Clump Settings")
        gbox_clump_generation_settings.setLayout(
            self.clump_generation_settings_ui.layout
        )
        self.main_layout.addWidget(gbox_clump_generation_settings)

        self.billboard_settings_ui = BillboardSettings()
        gbox_billboard_settings = QGroupBox("Billboard Settings")
        gbox_billboard_settings.setLayout(self.billboard_settings_ui.layout)
        self.main_layout.addWidget(gbox_billboard_settings)

        self.btn_generate_clump = QPushButton("Generate Clump")
        self.btn_generate_clump.clicked.connect(self.on_generate_clump_pressed)
        self.main_layout.addWidget(self.btn_generate_clump)

    def on_generate_clump_pressed(self):
        main.generate_clump()

    def get_foliage_values_arr(
        self, foliage_slider_arr: list[SliderSpinBox]
    ) -> list[int]:
        foliage_values = []
        for slider in foliage_slider_arr:
            foliage_values.append(slider.get_slider_value())
        return foliage_values
