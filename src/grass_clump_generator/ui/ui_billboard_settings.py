from PySide2.QtWidgets import *
from grass_clump_generator.ui.ui_slider_spinbox import SliderSpinBox
from grass_clump_generator.ui import ui_utils


class BillboardSettings(QLayout):
    def __init__(self):
        self.layout = self.create_layout(self.create_widgets())

    def create_widgets(self):

        self.cbox_render_billboard = QCheckBox("Render Billboard")
        self.cbox_render_billboard.stateChanged.connect(
            lambda: self.enable_options(self.cbox_render_billboard.isChecked())
        )

        layout_export_name = QHBoxLayout()
        lbl_export_name = QLabel("Base name")
        self.le_export_name = QLineEdit("billboard")
        self.le_export_name.setEnabled(False)
        layout_export_name.addWidget(lbl_export_name)
        layout_export_name.addWidget(self.le_export_name)

        layout_res = QHBoxLayout()
        lbl_res = QLabel("Resolution")
        self.le_res_width = QLineEdit("512")
        self.le_res_width.setEnabled(False)
        lbl_x = QLabel("x")
        self.le_res_height = QLineEdit("512")
        self.le_res_height.setEnabled(False)
        layout_res.addWidget(lbl_res)
        layout_res.addWidget(self.le_res_width)
        layout_res.addWidget(lbl_x)
        layout_res.addWidget(self.le_res_height)

        widgets = [self.cbox_render_billboard, layout_export_name, layout_res]
        return widgets

    def create_layout(self, objects):
        layout = QVBoxLayout()
        for object in objects:
            if isinstance(object, QWidget):
                layout.addWidget(object)
            elif isinstance(object, QLayout):
                layout.addLayout(object)
        return layout

    ## Listeners
    def enable_options(self, new_state):
        self.le_res_width.setEnabled(new_state)
        self.le_res_height.setEnabled(new_state)
        self.le_export_name.setEnabled(new_state)

    def get_render_enabled(self) -> bool:
        return self.cbox_render_billboard.isChecked()

    def get_resolution(self) -> list[int]:
        return [self.le_res_width.value(), self.le_res_height.value()]

    def get_base_name(self) -> str:
        return self.le_export_name.value()
