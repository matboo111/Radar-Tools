import threading
import time

class ObjectCache:
    def __init__(self):
        self.lock = threading.Lock()

        self.current_cycle_objects = {}
        self.display_objects = {}

        self.last_cycle_time = 0
        self.cycle_timeout = 3.0  # segundos

        self.last_config = {}
        self.last_firmware = {}

        self.mode = "object"

    def update(self, arbitration_id, decoded):

        with self.lock:

            arb = arbitration_id & 0xFFF

            if self.mode == "object":
                # 0x201 → configuração
                if arb == 0x201:
                    self.last_config = decoded
                    return

                # 0x700 → firmware
                if arb == 0x700:
                    self.last_firmware = decoded
                    return

                # 🔹 0x60A → início de novo ciclo
                if arb == 0x60A:
                    self._start_new_cycle(decoded)
                    return

                # 🔹 0x60B/C/D → dados de objeto
                if arb in (0x60B, 0x60C, 0x60D):

                    oid = decoded.get("Obj_ID")
                    if oid is None:
                        return

                    if oid not in self.current_cycle_objects:
                        self.current_cycle_objects[oid] = {"Obj_ID": oid}

                    self.current_cycle_objects[oid].update(decoded)

            elif self.mode == "cluster":
                if arb == 0x600:  # header cluster
                    self._start_new_cycle(decoded)
                    return

                if arb in (0x701, 0x702):  # dados cluster
                    cid = decoded.get("Cluster_ID")

                    if cid is None:
                        return

                    if cid not in self.current_cycle_objects:
                        self.current_cycle_objects[cid] = {"Cluster_ID": cid}

                    self.current_cycle_objects[cid].update(decoded)

    def _start_new_cycle(self, decoded):
        """
        Chamado quando chega 0x60A ou 0x701, indicando que um novo ciclo de dados está começando.
        Finaliza ciclo anterior e inicia novo.
        """

        # Finaliza ciclo anterior
        self.display_objects = self.current_cycle_objects.copy()

        # Inicia novo ciclo
        self.current_cycle_objects = {}

        self.last_cycle_time = time.time()

        self.nof_objects = decoded.get("Obj_NofObjects", 0)

    def snapshot(self):
        with self.lock:

            # Se radar parou de enviar, limpa
            if time.time() - self.last_cycle_time > self.cycle_timeout:
                self.display_objects = {}

            return self.display_objects.copy()

    def get_object_count(self):
        with self.lock:
            return getattr(self, "nof_objects", 0)
        
    def set_mode(self, mode):
        with self.lock:
            self.mode = mode

            # limpa dados ao trocar modo
            self.current_cycle_objects = {}
            self.display_objects = {}
