from PySide2.QtWidgets import *
from grass_clump_generator.ui.ui_slider_spinbox import SliderSpinBox
from grass_clump_generator.ui import ui_utils


class ClumpGenerationSettingsUI(QLayout):
    def __init__(self):
        self.create_widgets()
        self.layout = self.create_layout()

    def create_widgets(self):
        self.lbl_total_foliage = QLabel("Total Foliage Meshes")
        self.sbox_total_foliage = QSpinBox()
        self.sbox_total_foliage.setMaximum(1000)
        self.sbox_total_foliage.setValue(
            int(ui_utils.load_persistent_ui_val(5, self.lbl_total_foliage.text()))
        )
        self.sbox_total_foliage.valueChanged.connect(
            lambda: ui_utils.store_ui_value(
                self.sbox_total_foliage, self.lbl_total_foliage.text()
            )
        )

        self.lbl_radius = QLabel("Radius")
        self.sbox_radius = QSpinBox()
        self.sbox_radius.setMaximum(1000)
        self.sbox_radius.setValue(
            int(ui_utils.load_persistent_ui_val(10, self.lbl_radius.text()))
        )
        self.sbox_radius.valueChanged.connect(
            lambda: ui_utils.store_ui_value(self.sbox_radius, self.lbl_radius.text())
        )

        self.lbl_rot = QLabel("Rotation Variation")
        self.sld_sbox_rot = SliderSpinBox("Rotation Variation", 0, 360, 360)
        self.sld_sbox_scale_variance = SliderSpinBox("Scale Variation", 0, 100, 50)
        self.sld_sbox_scale_distance = SliderSpinBox("Scale by Radius", 0, 100, 50)

    def create_layout(self):
        layout_total_foliage = QHBoxLayout()
        layout_total_foliage.addWidget(self.lbl_total_foliage)
        layout_total_foliage.addWidget(self.sbox_total_foliage)

        layout_radius = QHBoxLayout()
        layout_radius.addWidget(self.lbl_radius)
        layout_radius.addWidget(self.sbox_radius)

        layout_settings = QVBoxLayout()
        layout_settings.addLayout(layout_total_foliage)
        layout_settings.addLayout(layout_radius)
        layout_settings.addLayout(self.sld_sbox_rot.get_sliderspinbox_layout())
        layout_settings.addLayout(
            self.sld_sbox_scale_variance.get_sliderspinbox_layout()
        )
        layout_settings.addLayout(
            self.sld_sbox_scale_distance.get_sliderspinbox_layout()
        )
        return layout_settings
