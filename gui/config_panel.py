from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QSpinBox

class ConfigPanel(QWidget):
    def __init__(self, can_manager, decoder):
        super().__init__()
        self.can_manager = can_manager
        self.decoder = decoder

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Max Distance (m):"))

        self.distance_spin = QSpinBox()
        self.distance_spin.setRange(50, 300)
        self.distance_spin.setValue(200)

        self.send_button = QPushButton("Send Config")
        self.send_button.clicked.connect(self.send_config)

        layout.addWidget(self.distance_spin)
        layout.addWidget(self.send_button)

        self.setLayout(layout)

    def send_config(self):
        frame_id, data = self.decoder.encode(
            "RadarCfg",
            {"RadarCfg_MaxDistance": self.distance_spin.value()}
        )
        self.can_manager.send_message(frame_id, data)
