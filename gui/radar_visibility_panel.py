from PyQt6.QtWidgets import QWidget, QVBoxLayout, QCheckBox, QLabel
from PyQt6.QtCore import pyqtSignal


class RadarVisibilityPanel(QWidget):

    visibility_changed = pyqtSignal(list)

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Radar Visibility"))

        self.checkboxes = []

        for i in range(8):
            cb = QCheckBox(f"Radar {i}")
            cb.setChecked(True)
            cb.stateChanged.connect(self.emit_change)

            self.checkboxes.append(cb)
            layout.addWidget(cb)

    # -----------------------------------------

    def emit_change(self):

        active = [
            i for i, cb in enumerate(self.checkboxes)
            if cb.isChecked()
        ]

        self.visibility_changed.emit(active)