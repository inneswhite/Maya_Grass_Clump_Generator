from PySide2.QtWidgets import *
from grass_clump_generator.ui.ui_slider_spinbox import SliderSpinBox
from grass_clump_generator.ui import ui_utils
from grass_clump_generator.data import persistent_settings as ps


class BillboardSettings(QLayout):
    def __init__(self):
        self.layout = self.create_layout(self.create_widgets())

    def create_widgets(self):

        self.cbox_render_billboard = QCheckBox("Render Billboard")

        self.cbox_render_billboard.setChecked(
            ps.read_value(ps.HEADER_UI_VALUES, "render_enabled")
        )
        self.cbox_render_billboard.stateChanged.connect(
            lambda: self.toggle_options(self.cbox_render_billboard.isChecked())
        )

        layout_export_name = QHBoxLayout()
        lbl_export_name = QLabel("Base name")
        self.le_export_name = QLineEdit("billboard")
        self.le_export_name.setEnabled(self.cbox_render_billboard.isChecked())
        if ps.read_value(ps.HEADER_UI_VALUES, "export_name"):
            self.le_export_name.setText(
                str(ps.read_value(ps.HEADER_UI_VALUES, "export_name"))
            )

        self.le_export_name.textChanged.connect(
            lambda: ps.write_value(
                ps.HEADER_UI_VALUES, "export_name", self.le_export_name.text()
            )
        )
        layout_export_name.addWidget(lbl_export_name)
        layout_export_name.addWidget(self.le_export_name)

        # Resolution Widgets
        layout_res = QHBoxLayout()
        lbl_res = QLabel("Resolution")
        self.le_res_width = QLineEdit("512")
        self.le_res_width.setEnabled(self.cbox_render_billboard.isChecked())
        self.le_res_width.textChanged.connect(
            lambda: ps.write_value(
                ps.HEADER_UI_VALUES, "res_width", self.le_res_width.text()
            )
        )
        self.le_res_width.setText(ui_utils.load_persistent_ui_val("512", "res_width"))

        lbl_x = QLabel("x")

        self.le_res_height = QLineEdit("512")
        self.le_res_height.setEnabled(self.cbox_render_billboard.isChecked())
        self.le_res_height.textChanged.connect(
            lambda: ps.write_value(
                ps.HEADER_UI_VALUES, "res_height", self.le_res_height.text()
            )
        )
        self.le_res_height.setText(ui_utils.load_persistent_ui_val("512", "res_height"))

        # Add widgets to layout
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
    def toggle_options(self, new_state):
        ps.write_value(ps.HEADER_UI_VALUES, "render_enabled", str(new_state))

        self.le_res_width.setEnabled(new_state)
        self.le_res_height.setEnabled(new_state)
        self.le_export_name.setEnabled(new_state)

    def get_render_enabled(self) -> bool:
        return self.cbox_render_billboard.isChecked()

    def get_resolution(self) -> list[int]:
        return [self.le_res_width.value(), self.le_res_height.value()]

    def get_base_name(self) -> str:
        return self.le_export_name.value()
