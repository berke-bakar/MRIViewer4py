from PySide6.QtWidgets import QApplication
from MainWindow import MainWindow
import sys

app = QApplication(sys.argv)

window = MainWindow(app)
window.resize(1200, 800)
window.show()

app.exec()