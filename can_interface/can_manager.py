import can
from PyQt6.QtCore import QObject, pyqtSignal, QThread

class CANWorker(QThread):
    message_received = pyqtSignal(object)

    def __init__(self, bus):
        super().__init__()
        self.bus = bus
        self.running = True

    def run(self):
        print("CAN Worker started")

        while self.running:
            try:
                # Processa múltiplos frames por ciclo
                for _ in range(50):
                    msg = self.bus.recv(timeout=0)
                    if msg is None:
                        break

                    self.message_received.emit(msg)

                self.msleep(1)

            except Exception as e:
                print(f"CAN thread error: {e}")
                self.msleep(100)

        print("CAN Worker stopped")

    def stop(self):
        self.running = False


class CANManager(QObject):
    message_received = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.bus = None
        self.worker = None

    def connect(self, channel="PCAN_USBBUS1", bitrate=500000, interface="pcan"):
        self.bus = can.interface.Bus(
            interface=interface,
            channel=channel,
            bitrate=bitrate
        )

        self.worker = CANWorker(self.bus)
        self.worker.message_received.connect(self.message_received)
        self.worker.start()

    def disconnect(self):
        if self.worker:
            self.worker.stop()
            self.worker.wait()
        if self.bus:
            self.bus.shutdown()

    def send_message(self, arbitration_id, data):
        msg = can.Message(
            arbitration_id=arbitration_id,
            data=data,
            is_extended_id=False
        )
        self.bus.send(msg)
