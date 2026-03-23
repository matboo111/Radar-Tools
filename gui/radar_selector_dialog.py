from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QCheckBox,
    QPushButton, QLabel
)


class RadarSelectorDialog(QDialog):

    def __init__(self, object_cache, cluster_cache):
        super().__init__()

        self.setWindowTitle("Select Active Radars")

        self.object_cache = object_cache
        self.cluster_cache = cluster_cache

        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Select Radar IDs"))

        self.checkboxes = []

        for i in range(8):
            cb = QCheckBox(f"Radar {i}")
            cb.setChecked(True)
            self.checkboxes.append(cb)
            layout.addWidget(cb)

        apply_btn = QPushButton("Apply")
        apply_btn.clicked.connect(self.apply_selection)

        layout.addWidget(apply_btn)

    # -----------------------------------------

    def apply_selection(self):

        active = [
            i for i, cb in enumerate(self.checkboxes)
            if cb.isChecked()
        ]

        self.object_cache.set_active_radars(active)
        self.cluster_cache.set_active_radars(active)

        self.accept()