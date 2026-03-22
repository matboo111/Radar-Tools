import threading
import time
from processing.numeric_filter import NumericFilter

class ClusterCache:
    def __init__(self):
        self.lock = threading.Lock()

        self.current_cycle_clusters = {}
        self.display_clusters = {}

        self.last_cycle_time = 0
        self.cycle_timeout = 3.0

        self.filter = NumericFilter()

    # -----------------------------------------

    def update(self, arbitration_id, decoded):

        with self.lock:

            arb = arbitration_id & 0xFFF

            if arb == 0x201:
                    self.last_config = decoded
                    return

            if arb == 0x600:
                self._start_new_cycle(decoded)
                return

            # 🔹 Dados de cluster
            if arb in (0x701, 0x702):

                cid = decoded.get("Cluster_ID")
                if cid is None:
                    return

                if cid not in self.current_cycle_clusters:
                    self.current_cycle_clusters[cid] = {"Cluster_ID": cid}

                self.current_cycle_clusters[cid].update(decoded)

    # -----------------------------------------

    def _start_new_cycle(self, decoded):

        self.display_clusters = self.current_cycle_clusters.copy()
        self.current_cycle_clusters = {}

        self.last_cycle_time = time.time()
        self.nof_clusters = decoded.get("Cluster_NofClusters", 0)

    # -----------------------------------------

    def snapshot(self):

        with self.lock:

            if time.time() - self.last_cycle_time > self.cycle_timeout:
                return {}
            
            data = self.display_clusters.copy()

        return self.filter.apply_cluster(data)

    # -----------------------------------------

    def get_cluster_count(self):
        with self.lock:
            return getattr(self, "nof_clusters", 0)