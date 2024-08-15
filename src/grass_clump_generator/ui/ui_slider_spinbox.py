from PySide2.QtWidgets import *
from PySide2.QtCore import Qt
import grass_clump_generator.data.persistent_settings as ps


class SliderSpinBox(QWidget):
    def __init__(self, name: str, min: int, max: int, value: int):
        self.value = value
        self.name = name

        self.label = QLabel(name)
        self.label.setMinimumWidth(100)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(min)
        self.slider.setMaximum(max)

        self.slider.valueChanged.connect(self.on_slider_changed)

        self.spinbox = QSpinBox()
        self.spinbox.setMinimumWidth(50)
        self.spinbox.setMinimum(min)
        self.spinbox.setMaximum(max)

        self.spinbox.valueChanged.connect(self.on_spinbox_changed)

        self.set_default_values()

        self.layout_sliderspinbox = QHBoxLayout()
        self.layout_sliderspinbox.addWidget(self.label)
        self.layout_sliderspinbox.addWidget(self.slider)
        self.layout_sliderspinbox.addWidget(self.spinbox)

    def on_slider_changed(self):
        self.spinbox.setValue(self.slider.value())
        ps.write_value(ps.HEADER_UI_VALUES, self.name, str(self.slider.value()))

    def on_spinbox_changed(self):
        self.slider.setValue(self.spinbox.value())
        ps.write_value(ps.HEADER_UI_VALUES, self.name, str(self.spinbox.value()))

    def get_sliderspinbox_layout(self):
        return self.layout_sliderspinbox

    def get_slider(self) -> QSlider:
        return self.slider

    def get_slider_value(self) -> int:
        return self.slider.value()

    def get_spinbox(self) -> QSpinBox:
        return self.spinbox

    def set_default_values(self):
        # Check if values already exist in ini file. If not, write in the initial default value
        if ps.read_value(ps.HEADER_UI_VALUES, self.name):
            self.value = int(ps.read_value(ps.HEADER_UI_VALUES, self.name))
        else:
            ps.write_value(ps.HEADER_UI_VALUES, self.name, self.value)

        self.slider.setValue(self.value)
        self.spinbox.setValue(self.value)
