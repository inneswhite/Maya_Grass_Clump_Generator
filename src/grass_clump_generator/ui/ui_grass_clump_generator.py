from PySide2.QtWidgets import *
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
from grass_clump_generator.ui import ui_utils
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
        import pymel.core as pm

        self.btn_select_foliage.setHidden(True)

        gbox_foliage_distributions = QGroupBox("Foliage Distributions")
        self.foliage_distribution_ui = FoliageDistributionsUI(pm.selected())
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
        self.main_layout.addWidget(self.btn_generate_clump)

    def on_generate_clump_pressed(self):
        from grass_clump_generator.clump_generator import GrassClumpGenerator

        self.grass_clump_generator = GrassClumpGenerator(
            foliage_arr=self.transform_selection,
            total_foliage_count=self.sbox_total_foliage.value(),
            foliage_values=self.get_foliage_values_arr(self.sliderspinbox_foliage_arr),
            distribution_radius=self.sbox_radius.value(),
            rotation_variation=self.sld_sbox_rot.get_slider_value(),
            scale_variation=self.sld_sbox_scale_variance.get_slider_value(),
            scale_distance=self.sld_sbox_scale_distance.get_slider_value(),
            render_billboards=self.billboard_settings_ui.get_render_enabled(),
        )
        self.grass_clump_generator.generate()

    def get_foliage_values_arr(
        self, foliage_slider_arr: list[SliderSpinBox]
    ) -> list[int]:
        foliage_values = []
        for slider in foliage_slider_arr:
            foliage_values.append(slider.get_slider_value())
        return foliage_values
