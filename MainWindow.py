from enum import Enum
import numpy as np
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QToolBar, QPushButton, QStatusBar, QMessageBox, QFileDialog

from MriViewer import MriViewer


class MainWindow(QMainWindow):

    class ButtonEnableOptions(Enum):
        DISABLE_BOTH = 0,
        DISABLE_NEXT = 1,
        DISABLE_PREV = 2,
        ENABLE_BOTH = 3

    def __init__(self, app):
        super().__init__()
        self.app = app  # declare an app member
        self.setWindowTitle("MRIViewer4py")
        self.version = "0.0.2"  # Don't forget to update here after each PR

        # Menubar and menus
        menu_bar = self.menuBar()
        # File menu and it's actions
        file_menu = menu_bar.addMenu("File")
        load_action = file_menu.addAction("Load .npy file")
        load_action.setShortcut("Ctrl+O")
        load_action.setStatusTip("Open .npy file")
        load_action.triggered.connect(self.load_npy_file_action_handler)
        quit_action = file_menu.addAction("Quit")
        quit_action.setShortcut("Ctrl+Q")
        quit_action.setStatusTip("Quit the application")
        quit_action.triggered.connect(self.quit_app_action_handler)
        # Edit menu and it's actions
        edit_menu = menu_bar.addMenu("Control")
        self.prev_image_action = edit_menu.addAction("Previous Image")
        self.prev_image_action.triggered.connect(self.prev_image_action_handler)
        self.prev_image_action.setShortcut(Qt.Key.Key_Left)
        self.next_image_action = edit_menu.addAction("Next Image")
        self.next_image_action.setShortcut(Qt.Key.Key_Right)
        self.next_image_action.triggered.connect(self.next_image_action_handler)

        help_menu = menu_bar.addMenu("Help")

        about_action = help_menu.addAction("About")
        about_action.triggered.connect(self.about_action_handler)

        version_action = help_menu.addAction("Version")
        version_action.triggered.connect(self.version_action_handler)

        # Working with status bars
        self.setStatusBar(QStatusBar(self))
        self.mri_viewer = MriViewer()
        self.mri_viewer.add_event_listener("prevButtonPressed", self.prev_image_action_handler)
        self.mri_viewer.add_event_listener("nextButtonPressed", self.next_image_action_handler)
        self.next_image_action.setDisabled(True)
        self.prev_image_action.setDisabled(True)
        self.setCentralWidget(self.mri_viewer)

    def load_npy_file_action_handler(self):
        name = QFileDialog.getOpenFileName(self, "Open a .npy file", filter="Numpy array (*.npy);")
        if name != ('', ''):
            self.mri_viewer.update_image_data(np.load(name[0]))
            self.statusBar().showMessage("File loaded, you can browse the images now", 5000)
            self.prev_image_action.setDisabled(True)
            self.next_image_action.setDisabled(False)

    def quit_app_action_handler(self):
        self.app.quit()

    def prev_image_action_handler(self):
        self.mri_viewer.current_img_index -= 1
        disable_status = self.ButtonEnableOptions.DISABLE_PREV
        if self.mri_viewer.current_img_index < 0:
            self.mri_viewer.current_img_index = 0

        # if first picture disable prev button
        if self.mri_viewer.current_img_index == 0:
            disable_status = self.ButtonEnableOptions.DISABLE_PREV
        else:
            disable_status = self.ButtonEnableOptions.ENABLE_BOTH

        self.refresh_and_enable(disable_status)

    def next_image_action_handler(self):
        self.mri_viewer.current_img_index += 1
        disable_status = self.ButtonEnableOptions.DISABLE_PREV
        if self.mri_viewer.current_img_index >= self.mri_viewer.current_img_data.shape[2]:
            self.mri_viewer.current_img_index = self.mri_viewer.current_img_data.shape[2] - 1

        # if last picture disable next button
        if self.mri_viewer.current_img_index == (self.mri_viewer.current_img_data.shape[2] - 1):
            disable_status = self.ButtonEnableOptions.DISABLE_NEXT
        else:
            disable_status = self.ButtonEnableOptions.ENABLE_BOTH

        self.refresh_and_enable(disable_status)

    def refresh_and_enable(self, disable_status):
        if disable_status == self.ButtonEnableOptions.DISABLE_BOTH:
            self.mri_viewer.next_button.setDisabled(True)
            self.mri_viewer.prev_button.setDisabled(True)
        elif disable_status == self.ButtonEnableOptions.DISABLE_NEXT:
            self.mri_viewer.next_button.setDisabled(True)
            self.mri_viewer.prev_button.setDisabled(False)
        elif disable_status == self.ButtonEnableOptions.DISABLE_PREV:
            self.mri_viewer.next_button.setDisabled(False)
            self.mri_viewer.prev_button.setDisabled(True)
        else:
            self.mri_viewer.next_button.setDisabled(False)
            self.mri_viewer.prev_button.setDisabled(False)

        self.mri_viewer.refresh_shown_image()

        self.next_image_action.setDisabled(not self.mri_viewer.next_button.isEnabled())
        self.prev_image_action.setDisabled(not self.mri_viewer.prev_button.isEnabled())

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
