from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QDialog, QTextEdit, QPushButton
from gui.connection_panel import ConnectionPanel
from gui.live_view import LiveView
from gui.radar_view import RadarView
from gui.config_panel import ConfigPanel
from can_interface.can_manager import CANManager
from can_interface.dbc_decoder import DBCDecoder
from processing.object_cache import ObjectCache
from PyQt6.QtCore import QTimer


DBC_FILES = [
    "resources/ARS408_can_database_ch0-new.dbc",
    "resources/ARS408_can_database_ch1-new.dbc",
    "resources/ARS408_can_database_ch2-new.dbc",
    "resources/ARS408_can_database_ch3-new.dbc",
    "resources/ARS408_can_database_ch4-new.dbc",
    "resources/ARS408_can_database_ch5-new.dbc",
    "resources/ARS408_can_database_ch6-new.dbc",
    "resources/ARS408_can_database_ch7-new.dbc",
    "resources/canmod-gps.dbc"
]

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Radar Configuration Tool")
        self.resize(1200, 700)

        self.can_manager = CANManager()
        self.decoder = DBCDecoder(DBC_FILES)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        self.connection_panel = ConnectionPanel(self.can_manager)
        self.connection_panel.show_config_requested.connect(
            self.show_config_dialog
        )

        self.connection_panel.show_firmware_requested.connect(
            self.show_firmware_dialog
        )
        self.connection_panel.mode_changed.connect(self.on_mode_changed)

        self.config_panel = ConfigPanel(self.can_manager, self.decoder)
        self.live_view = LiveView()
        self.radar_view = RadarView()

        left_layout.addWidget(self.connection_panel)
        left_layout.addWidget(self.config_panel)

        right_layout.addWidget(self.radar_view)
        right_layout.addWidget(self.live_view)

        main_layout.addLayout(left_layout, 1)
        main_layout.addLayout(right_layout, 3)

        central_widget.setLayout(main_layout)

        self.cache = ObjectCache()

        self.can_manager.message_received.connect(self.handle_message)

        # Timer de atualização da GUI (20 Hz)
        self.gui_timer = QTimer()
        self.gui_timer.timeout.connect(self.update_gui)
        self.gui_timer.start(50)

    def handle_message(self, msg):

        msg_name, decoded = self.decoder.decode(msg)

        if decoded is None:
            return

        self.cache.update(msg.arbitration_id, decoded)
    
    def update_gui(self):

        snapshot = self.cache.snapshot()

        self.live_view.update_table_bulk(snapshot)
        self.radar_view.update_plot_bulk(snapshot)

        count = self.cache.get_object_count()
        self.statusBar().showMessage(
            f"Objects detected: {count}"
        )

    def show_config_dialog(self):

        data = getattr(self.cache, "last_config", None)

        dialog = QDialog(self)
        dialog.setWindowTitle("Radar Configuration (0x201)")
        dialog.resize(500, 400)

        layout = QVBoxLayout()

        text = QTextEdit()
        text.setReadOnly(True)

        if data:
            formatted = "\n".join(f"{k}: {v}" for k, v in data.items())
        else:
            formatted = "No configuration frame received yet."

        text.setText(formatted)

        close_button = QPushButton("Close")
        close_button.clicked.connect(dialog.close)

        layout.addWidget(text)
        layout.addWidget(close_button)

        dialog.setLayout(layout)
        dialog.exec()

    def show_firmware_dialog(self):

        data = getattr(self.cache, "last_firmware", None)

        dialog = QDialog(self)
        dialog.setWindowTitle("Radar Firmware Info (0x700)")
        dialog.resize(500, 400)

        layout = QVBoxLayout()

        text = QTextEdit()
        text.setReadOnly(True)

        if data:
            formatted = "\n".join(f"{k}: {v}" for k, v in data.items())
        else:
            formatted = "No firmware frame received yet."

        text.setText(formatted)

        close_button = QPushButton("Close")
        close_button.clicked.connect(dialog.close)

        layout.addWidget(text)
        layout.addWidget(close_button)

        dialog.setLayout(layout)
        dialog.exec()

    def on_mode_changed(self, mode):

        print("Switching mode to:", mode)

        self.object_cache.set_mode(mode)
