from PyQt5.QtWidgets import QApplication, QFrame, QMainWindow

from models import Camera
from views import StartWindow
import sys

camera = Camera(0)
camera.initialize()

w = 900; h = 600
app = QApplication([])
start_window = StartWindow(camera)
start_window.resize(w, h)
start_window.show()
app.exit(app.exec_())