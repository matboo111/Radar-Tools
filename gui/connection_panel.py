from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QComboBox, QLineEdit
)
from PyQt6.QtCore import Qt, pyqtSignal

from processing.radar_mode import RadarMode

class ConnectionPanel(QWidget):

    show_config_requested = pyqtSignal()
    show_firmware_requested = pyqtSignal()
    mode_changed = pyqtSignal(RadarMode)

    def __init__(self, can_manager):

        super().__init__()
        self.can_manager = can_manager

        layout = QVBoxLayout()

        title = QLabel("CAN Connection")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Interface Selection
        self.interface_combo = QComboBox()
        self.interface_combo.addItems([
            "pcan",
            "socketcan"
        ])

        # Channel input
        self.channel_input = QComboBox() #QLineEdit("can0")
        self.channel_input.addItems([
            "PCAN_USBBUS1",
            "can1",
            "can0",
            "vcan0"
        ])

        # Bitrate input
        self.bitrate_input = QComboBox() #QLineEdit("can0")
        self.bitrate_input.addItems([
            "500000",
            "250000",
            "1000000"
        ])

        # Buttons
        self.connect_button = QPushButton("Connect")
        self.disconnect_button = QPushButton("Disconnect")
        self.disconnect_button.setEnabled(False)

        self.config_button = QPushButton("Radar Config (0x201)")
        self.firmware_button = QPushButton("Firmware Info (0x700)")

        self.mode_button = QPushButton("Switch to Cluster Mode")
        self.mode_button.clicked.connect(self.toggle_mode)

        self.status_label = QLabel("Status: Disconnected")

        layout.addWidget(self.config_button)
        layout.addWidget(self.firmware_button)
        layout.addWidget(self.mode_button)

        layout.addWidget(QLabel("Interface"))
        layout.addWidget(self.interface_combo)

        layout.addWidget(QLabel("Channel"))
        layout.addWidget(self.channel_input)

        layout.addWidget(QLabel("Bitrate"))
        layout.addWidget(self.bitrate_input)

        layout.addWidget(self.connect_button)
        layout.addWidget(self.disconnect_button)
        layout.addWidget(self.status_label)

        self.setLayout(layout)

        # Connections
        self.connect_button.clicked.connect(self.connect_can)
        self.disconnect_button.clicked.connect(self.disconnect_can)

        self.config_button.clicked.connect(self.show_config_requested.emit)

        self.firmware_button.clicked.connect(
            self.show_firmware_requested.emit
        )

    def connect_can(self):
        interface = self.interface_combo.currentText()
        channel = self.channel_input.currentText()
        bitrate = int(self.bitrate_input.currentText())

        try:
            self.can_manager.connect(
                channel=channel,
                bitrate=bitrate,
                interface=interface
            )

            self.status_label.setText("Status: Connected")
            self.connect_button.setEnabled(False)
            self.disconnect_button.setEnabled(True)

        except Exception as e:
            self.status_label.setText(f"Error: {str(e)}")

    def disconnect_can(self):
        self.can_manager.disconnect()
        self.status_label.setText("Status: Disconnected")
        self.connect_button.setEnabled(True)
        self.disconnect_button.setEnabled(False)

    def toggle_mode(self):
        if self.mode_button.text() == "Switch to Cluster Mode":
            mode = RadarMode.CLUSTER
            self.mode_button.setText("Switch to Object Mode")
        else:
            mode = RadarMode.OBJECT
            self.mode_button.setText("Switch to Cluster Mode")

        self.mode_changed.emit(mode)
