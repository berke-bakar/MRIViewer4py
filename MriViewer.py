from PySide6.QtCore import QByteArray
from PySide6.QtGui import QPixmap, QImage, Qt, qRgb
from PySide6.QtWidgets import QPushButton, QWidget, QLabel, QGridLayout
import numpy as np


class MriViewer(QWidget):
    def __init__(self, img_data=None):
        super().__init__()
        self.current_img_index = 0
        self.current_img_data = img_data
        self.prev_button = QPushButton("Prev", self)
        self.prev_button.clicked.connect(self.prev_button_handler)
        self.next_button = QPushButton("Next", self)
        self.next_button.clicked.connect(self.next_button_handler)
        self.image_label = QLabel(self)
        self.image_label.resize(1080, 720)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if self.current_img_data is None:
            self.prev_button.setDisabled(True)
            self.next_button.setDisabled(True)
        self.refresh_shown_image()
        grid_layout = QGridLayout()
        grid_layout.addWidget(self.image_label, 0, 0, 4, 4)
        grid_layout.addWidget(self.prev_button, 4, 1, 1, 1)
        grid_layout.addWidget(self.next_button, 4, 2, 1, 1)
        grid_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(grid_layout)

    def prev_button_handler(self):
        self.current_img_index -= 1
        if self.current_img_index < 0:
            self.current_img_index = 0
        # if first picture disable prev button
        if self.current_img_index == 0:
            self.prev_button.setDisabled(True)
            self.next_button.setDisabled(False)
        else:
            self.prev_button.setDisabled(False)
            self.next_button.setDisabled(False)
        self.refresh_shown_image()

    def next_button_handler(self):
        self.current_img_index += 1
        if self.current_img_index >= self.current_img_data.shape[2]:
            self.current_img_index = self.current_img_data.shape[2] - 1
        # if last picture disable next button
        if self.current_img_index == (self.current_img_data.shape[2] - 1):
            self.next_button.setDisabled(True)
            self.prev_button.setDisabled(False)
        else:
            self.next_button.setDisabled(False)
            self.prev_button.setDisabled(False)
        self.refresh_shown_image()

    def update_image_data(self, new_img_data):
        self.current_img_data = new_img_data
        self.current_img_index = 0
        self.next_button.setDisabled(False)
        self.prev_button.setDisabled(True)
        self.refresh_shown_image()

    def refresh_shown_image(self):
        if self.current_img_data is not None:
            selected_img = self.current_img_data[:, :, self.current_img_index]
            selected_img = self.normalize8(selected_img)
        else:
            selected_img = np.zeros((720, 1080), dtype=np.uint8)

        height, width = selected_img.shape
        bytesPerLine = width
        qImg = QImage(np.ascontiguousarray(selected_img.data), width, height, bytesPerLine,
                      QImage.Format.Format_Grayscale8)
        pixmap = QPixmap.fromImage(qImg)
        pixmap = pixmap.scaledToHeight(720, Qt.TransformationMode.FastTransformation)

        self.image_label.resize(pixmap.width(), pixmap.height())
        self.image_label.setPixmap(pixmap)

    def normalize8(self, img):
        mn = img.min()
        mx = img.max()
        mx -= mn
        if mx == 0:
            img = np.zeros((img.shape[0], img.shape[1]))
        else:
            img = ((img - mn) / mx) * 255
        return img.astype(np.uint8)
