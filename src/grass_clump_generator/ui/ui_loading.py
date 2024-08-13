import grass_clump_generator.ui.ui_utils as ui_utils
import grass_clump_generator.ui.ui_manager
from PySide2.QtWidgets import *
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
import threading
import maya.utils
import grass_clump_generator.main as main


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

        self.closeEvent = self.on_close
        self.is_open = True

        self.create_widgets()
        self.create_layout()

        self.ellipses = ""
        self.initialise_loading_anim()

        self.pymel_timer = threading.Timer(1, self.import_pymel)
        self.pymel_timer.start()

    def create_widgets(self):
        self.lbl_loading_message = QLabel(self.loading_message)

    def create_layout(self):
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.lbl_loading_message)
        self.setLayout(self.main_layout)

    def initialise_loading_anim(self):
        if self.is_open:
            self.timer = threading.Timer(0.5, self.initialise_loading_anim)

            self.timer.start()
            self.lbl_loading_message.setText(self.loading_message + self.ellipses)
            if len(self.ellipses) >= 3:
                self.ellipses = ""
            else:
                self.ellipses += "."

    def import_pymel(self):
        print("importing pymel")
        maya.utils.executeInMainThreadWithResult(self.import_pymel_main_thread)

    def import_pymel_main_thread(self):
        import pymel.core

        main.tool_loaded()
        self.close()

    def on_close(self, event):
        self.is_open = False
