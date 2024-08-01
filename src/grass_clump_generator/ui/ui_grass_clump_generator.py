from PySide2.QtCore import Qt
from PySide2.QtWidgets import *
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
from grass_clump_generator.ui import ui_utils as ui_utils

from importlib import reload


class SliderSpinBox:
    def __init__(self, name: str, min: int, max: int, value: int):
        self.label = QLabel(name)
        self.label.setMinimumWidth(100)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(min)
        self.slider.setMaximum(max)
        self.slider.setValue(value)
        self.slider.valueChanged.connect(self.on_slider_changed)

        self.spinbox = QSpinBox()
        self.spinbox.setMinimumWidth(50)
        self.spinbox.setMinimum(min)
        self.spinbox.setMaximum(max)
        self.spinbox.setValue(value)
        self.spinbox.valueChanged.connect(self.on_spinbox_changed)

        self.layout_sliderspinbox = QHBoxLayout()
        self.layout_sliderspinbox.addWidget(self.label)
        self.layout_sliderspinbox.addWidget(self.slider)
        self.layout_sliderspinbox.addWidget(self.spinbox)

    def on_slider_changed(self):
        self.spinbox.setValue(self.slider.value())

    def on_spinbox_changed(self):
        self.slider.setValue(self.spinbox.value())

    def get_sliderspinbox_layout(self):
        return self.layout_sliderspinbox

    def get_slider(self) -> QSlider:
        return self.slider

    def get_slider_value(self) -> int:
        return self.slider.value()

    def get_spinbox(self) -> QSpinBox:
        return self.spinbox


class ClumpGeneratorUI(MayaQWidgetDockableMixin, QDialog):
    def __init__(self, parent=ui_utils.maya_main_window()):
        super(ClumpGeneratorUI, self).__init__(parent)
        self.setWindowTitle("Grass Clump Generator")
        self.setGeometry(100, 100, 300, 200)

        self.create_widgets()
        self.setup_connections()
        self.create_layouts()

    def create_widgets(self):
        self.btn_select_foliage = QPushButton("Get Foliage From Selection")

    def setup_connections(self):
        self.btn_select_foliage.clicked.connect(self.select_pressed)

    def create_layouts(self):

        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.btn_select_foliage)

        self.setLayout(self.main_layout)

    ## UI Methods after a foliage selection has been made

    def post_sel_create_widgets(self):
        self.create_foliage_sliders(self.transform_selection)

        self.lbl_total_foliage = QLabel("Total Foliage Meshes")
        self.sbox_total_foliage = QSpinBox()
        self.sbox_total_foliage.setMaximum(1000)
        self.sbox_total_foliage.setValue(5)

        self.gbox_distribution_settings = QGroupBox("Settings")
        self.lbl_radius = QLabel("Radius")
        self.sbox_radius = QSpinBox()
        self.sbox_radius.setMaximum(1000)
        self.sbox_radius.setValue(10)

        self.lbl_rot = QLabel("Rotation Variation")
        self.sld_sbox_rot = SliderSpinBox("Rotation Variation", 0, 360, 360)
        self.sld_sbox_scale_variance = SliderSpinBox("Scale Variation", 0, 100, 50)
        self.sld_sbox_scale_distance = SliderSpinBox("Scale by Radius", 0, 100, 50)

        self.btn_generate_clump = QPushButton("Generate Clump")

    def post_sel_setup_connections(self):
        self.btn_generate_clump.clicked.connect(self.on_generate_clump_pressed)

    def pose_sel_layouts(self):
        self.layout_total_foliage = QHBoxLayout()
        self.layout_total_foliage.addWidget(self.lbl_total_foliage)
        self.layout_total_foliage.addWidget(self.sbox_total_foliage)

        self.layout_radius = QHBoxLayout()
        self.layout_radius.addWidget(self.lbl_radius)
        self.layout_radius.addWidget(self.sbox_radius)

        self.layout_settings = QVBoxLayout()
        self.layout_settings.addLayout(self.layout_radius)
        self.layout_settings.addLayout(self.sld_sbox_rot.get_sliderspinbox_layout())
        self.layout_settings.addLayout(
            self.sld_sbox_scale_variance.get_sliderspinbox_layout()
        )
        self.layout_settings.addLayout(
            self.sld_sbox_scale_distance.get_sliderspinbox_layout()
        )
        self.gbox_distribution_settings.setLayout(self.layout_settings)

        self.main_layout.addLayout(self.layout_total_foliage)
        self.main_layout.addWidget(self.gbox_distribution_settings)
        self.main_layout.addWidget(self.btn_generate_clump)

    ## Dynamic UI
    def create_foliage_sliders(self, foliage_nodes):
        self.gbox_foliage = QGroupBox("Foliage Distribution Ratio")

        self.sliderspinbox_foliage_arr = []
        self.layout_foliage_group = QVBoxLayout()
        for foliage in foliage_nodes:
            # Create Widgets
            sliderspinbox = SliderSpinBox(foliage.name(), 0, 100, 100)

            self.sliderspinbox_foliage_arr.append(sliderspinbox)

            layout_foliage = sliderspinbox.get_sliderspinbox_layout()

            # Add layout to main
            self.layout_foliage_group.addLayout(layout_foliage)

        self.gbox_foliage.setLayout(self.layout_foliage_group)
        self.main_layout.addWidget(self.gbox_foliage)

    ## Listeners
    def select_pressed(self):
        self.transform_selection = pm.selected()
        self.post_sel_create_widgets()
        self.post_sel_setup_connections()
        self.pose_sel_layouts()

    def on_generate_clump_pressed(self):
        from grass_clump_generator.main import GrassClumpGenerator

        self.grass_clump_generator = GrassClumpGenerator(
            foliage_arr=self.transform_selection,
            total_foliage_count=self.sbox_total_foliage.value(),
            foliage_values=self.get_foliage_values_arr(self.sliderspinbox_foliage_arr),
            distribution_radius=self.sbox_radius.value(),
            rotation_variation=self.sld_sbox_rot.get_slider_value(),
            scale_variation=self.sld_sbox_scale_variance.get_slider_value(),
            scale_distance=self.sld_sbox_scale_distance.get_slider_value(),
        )
        self.grass_clump_generator.generate()

    def get_foliage_values_arr(
        self, foliage_slider_arr: list[SliderSpinBox]
    ) -> list[int]:
        foliage_values = []
        for slider in foliage_slider_arr:
            foliage_values.append(slider.get_slider_value())
        return foliage_values
