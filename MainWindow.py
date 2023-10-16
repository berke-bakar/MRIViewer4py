import numpy as np
from PySide6.QtCore import QSize
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QMainWindow, QToolBar, QPushButton, QStatusBar, QMessageBox, QFileDialog

from MriViewer import MriViewer


class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app  # declare an app member
        self.setWindowTitle("MRIViewer4py")
        self.version = "0.0.1"  # Don't forget to update here after each PR

        # Menubar and menus
        menu_bar = self.menuBar()
        # File menu and it's actions
        file_menu = menu_bar.addMenu("File")
        load_action = file_menu.addAction("Load .npy file")
        load_action.setShortcut("Ctrl+O")
        load_action.setStatusTip("Open .npy file")
        load_action.triggered.connect(self.load_npy_file_action_handler)
        quit_action = file_menu.addAction("Quit")
        quit_action.triggered.connect(self.quit_app_action_handler)
        # Edit menu and it's actions
        edit_menu = menu_bar.addMenu("Control")
        prev_image_action = edit_menu.addAction("Previous Image")
        prev_image_action.triggered.connect(self.prev_image_action_handler)
        next_image_action = edit_menu.addAction("Next Image")
        next_image_action.triggered.connect(self.next_image_action_handler)

        help_menu = menu_bar.addMenu("Help")

        about_action = help_menu.addAction("About")
        about_action.triggered.connect(self.about_action_handler)

        version_action = help_menu.addAction("Version")
        version_action.triggered.connect(self.version_action_handler)

        # Working with status bars
        self.setStatusBar(QStatusBar(self))
        self.mri_viewer = MriViewer()
        self.setCentralWidget(self.mri_viewer)

    def load_npy_file_action_handler(self):
        name = QFileDialog.getOpenFileName(self, "Open a .npy file", filter="Numpy array (*.npy);")
        if name != ('', ''):
            self.mri_viewer.update_image_data(np.load(name[0]))

    def quit_app_action_handler(self):
        self.app.quit()

    def prev_image_action_handler(self):
        if self.mri_viewer.prev_button.isEnabled():
            self.mri_viewer.prev_button_handler()

    def next_image_action_handler(self):
        if self.mri_viewer.next_button.isEnabled():
            self.mri_viewer.next_button_handler()

    def about_action_handler(self):
        # TODO: Fix github link
        ret = QMessageBox.information(self, "About MRIViewer4py",
                                      "This is a small project to visualize MRI images that are stored in .npy format "
                                      "files. You can load any .npy MRI images formatted in the following format: ("
                                      "height, width, slice index). For more information visit: (Github Link)",
                                      QMessageBox.StandardButton.Close)

    def version_action_handler(self):
        ret = QMessageBox.information(self, "Version Information",
                                      "Current version: " + self.version,
                                      QMessageBox.StandardButton.Close)
