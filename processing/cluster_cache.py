import threading
import time
from processing.numeric_filter import NumericFilter

class ClusterCache:
    def __init__(self):
        self.lock = threading.Lock()

        self.current_cycle_clusters = {} # {(rid, oid): obj}
        self.display_clusters = {}

        self.last_cycle_time = 0
        self.cycle_timeout = 3.0

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

    # -----------------------------------------

    def update(self, arbitration_id, decoded):

        with self.lock:

            radar_id = (arbitration_id >> 4) & 0xF
            msg_id = arbitration_id & 0xF0F

            r = self.radars[radar_id]

            if msg_id == 0x201:
                    self.last_config = decoded
                    return

            if msg_id == 0x600:
                r["display"] = r["current"].copy()
                r["current"] = {}
                r["last_cycle"] = time.time()
                #self._start_new_cycle(decoded)
                self.nof_clusters = decoded.get("Cluster_NofClusters", 0)
                return

            # 🔹 Dados de cluster
            if msg_id in (0x701, 0x702):

                cid = decoded.get("Cluster_ID")
                key = (radar_id, cid)
                if cid is None:
                    return

                if cid not in r["current"]:
                    r["current"][cid] = {
                        "Cluster_ID": cid,
                        "Radar_ID": radar_id
                    }

                r["current"][cid].update(decoded)
            if key not in self.current_cycle_clusters:
                self.current_cycle_clusters[key] = {
                    "Cluster_ID": cid,
                    "Radar_ID": radar_id
                }

            self.current_cycle_clusters[key].update(decoded)
    # -----------------------------------------

    def _start_new_cycle(self, decoded):

        self.display_clusters = {
            k: v for k, v in self.current_cycle_clusters.items()
        }
        self.current_cycle_clusters = {}

        self.last_cycle_time = time.time()
        self.nof_clusters = decoded.get("Cluster_NofClusters", 0)

    # -----------------------------------------

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

                for cid, obj in r["display"].items():

                    key = (rid, cid)
                    merged[key] = obj

        return self.filter.apply_cluster(merged)

    # -----------------------------------------

    def get_cluster_count(self):
        with self.lock:
            return getattr(self, "nof_clusters", 0)
        
    def set_active_radars(self, radar_ids):
        with self.lock:
            self.active_radars = set(radar_ids)