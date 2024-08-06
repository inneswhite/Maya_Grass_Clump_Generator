from PySide2.QtWidgets import *
from grass_clump_generator.ui.ui_slider_spinbox import SliderSpinBox


class FoliageDistributionsUI(QLayout):
    def __init__(self, source_foliage):
        self.foliage_widgets = self.create_slider_spinboxes(source_foliage)
        self.layout = self.create_layout(self.foliage_widgets)

    def create_slider_spinboxes(self, src_foliage) -> list[SliderSpinBox]:
        sliderspinbox_foliage_arr = []

        for foliage in src_foliage:
            sliderspinbox = SliderSpinBox(foliage.name(), 0, 100, 100)
            sliderspinbox_foliage_arr.append(sliderspinbox)

        return sliderspinbox_foliage_arr

    def create_layout(self, foliage_widgets: list[SliderSpinBox]) -> QLayout:
        layout = QVBoxLayout()
        for widget in foliage_widgets:
            layout.addLayout(widget.get_sliderspinbox_layout())
        return layout
