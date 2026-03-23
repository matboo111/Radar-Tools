import threading
import time
from processing.numeric_filter import NumericFilter

class ObjectCache:
    def __init__(self):
        self.lock = threading.Lock()

        self.current_cycle_objects = {} # {(rid, oid): obj}
        self.display_objects = {}

        self.last_cycle_time = 0
        self.cycle_timeout = 3.0  # segundos

        self.last_config = {}
        self.last_firmware = {}

        self.filter = NumericFilter()

        self.active_radars = set(range(8))  # todos ativos por padrão

        self.radars = {
            rid: {
                "current": {},
                "display": {},
                "last_cycle": 0
            }
            for rid in range(8)
        }

    def update(self, arbitration_id, decoded):

        with self.lock:

            radar_id = (arbitration_id >> 4) & 0xF
            msg_id = arbitration_id & 0xF0F

            r = self.radars[radar_id]

            # 0x201 → configuração
            if msg_id == 0x201:
                self.last_config = decoded
                return

            # 0x700 → firmware
            if msg_id == 0x700:
                self.last_firmware = decoded
                return

            # 🔹 0x60A → início de novo ciclo
            if msg_id == 0x60A:
                r["display"] = r["current"].copy()
                r["current"] = {}
                r["last_cycle"] = time.time()
                #self._start_new_cycle(decoded)
                self.nof_objects = decoded.get("Obj_NofObjects", 0)
                return

            # 🔹 0x60B/C/D → dados de objeto
            if msg_id in (0x60B, 0x60C, 0x60D):

                oid = decoded.get("Obj_ID")
                key = (radar_id, oid)
                if oid is None:
                    return

                if oid not in r["current"]:
                    r["current"][oid] = {
                        "Obj_ID": oid,
                        "Radar_ID": radar_id
                    }

                r["current"][oid].update(decoded)

            if key not in self.current_cycle_objects:
                self.current_cycle_objects[key] = {
                    "Obj_ID": oid,
                    "Radar_ID": radar_id
                }

            self.current_cycle_objects[key].update(decoded)

    def _start_new_cycle(self, decoded):
        """
        Chamado quando chega 0x60A ou 0x701, indicando que um novo ciclo de dados está começando.
        Finaliza ciclo anterior e inicia novo.
        """

        # Finaliza ciclo anterior
        self.display_objects = self.current_cycle_objects.copy()
        self.display_objects = {
            k: v for k, v in self.current_cycle_objects.items()
        }

        self.current_cycle_objects = {}

        self.last_cycle_time = time.time()

        self.nof_objects = decoded.get("Obj_NofObjects", 0)

    def snapshot(self):

        now = time.time()
        merged = {}

        with self.lock:

            for rid, r in self.radars.items():

                if rid not in self.active_radars:
                    continue

                # timeout por radar
                if now - r["last_cycle"] > self.cycle_timeout:
                    continue

                for oid, obj in r["display"].items():

                    key = (rid, oid)
                    merged[key] = obj

        return self.filter.apply_object(merged)

    def get_object_count(self):
        with self.lock:
            return getattr(self, "nof_objects", 0)
        
    def set_active_radars(self, radar_ids):
        with self.lock:
            self.active_radars = set(radar_ids)
            