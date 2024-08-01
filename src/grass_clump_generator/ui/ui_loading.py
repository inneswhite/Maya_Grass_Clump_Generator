import grass_clump_generator.ui.ui_utils as ui_utils
from PySide2.QtWidgets import *
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin


class LoadingBar(MayaQWidgetDockableMixin, QDialog):
    def __init__(
        self,
        parent=ui_utils.maya_main_window(),
        title="Loading",
        loading_message="Loading",
    ):
        super(LoadingBar, self).__init__(parent)
        self.setWindowTitle(title)
        self.setGeometry(100, 100, 150, 150)
        self.loading_message = loading_message

        self.create_widgets()
        self.create_layout()

    def create_widgets(self):
        self.lbl_loading_message = QLabel(self.loading_message)

    def create_layout(self):
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.lbl_loading_message)
        self.setLayout(self.main_layout)
