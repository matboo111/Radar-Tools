class NumericFilter:

    def __init__(self):
        self.enabled = False

        self.dist_long_min = None
        self.dist_long_max = None

        self.dist_lat_min = None
        self.dist_lat_max = None

        self.rcs_min = None
        self.rcs_max = None

        self.prob_min = None  # apenas object mode

    # -----------------------------------------

    def apply_object(self, objects):

        if not self.enabled:
            return objects

        filtered = {}

        for oid, obj in objects.items():

            if not self._passes_object(obj):
                continue

            filtered[oid] = obj

        return filtered

    # -----------------------------------------

    def apply_cluster(self, clusters):

        if not self.enabled:
            return clusters

        filtered = {}

        for cid, cl in clusters.items():

            if not self._passes_cluster(cl):
                continue

            filtered[cid] = cl

        return filtered

    # -----------------------------------------

    def _passes_object(self, obj):

        dl = obj.get("Obj_DistLong")
        dt = obj.get("Obj_DistLat")
        prob = obj.get("Obj_ProbOfExist")
        rcs = obj.get("Obj_RCS")

        if not self._in_range(dl, self.dist_long_min, self.dist_long_max):
            return False

        if not self._in_range(dt, self.dist_lat_min, self.dist_lat_max):
            return False

        if self.prob_min is not None and prob is not None:
            if prob < self.prob_min:
                return False

        if not self._in_range(rcs, self.rcs_min, self.rcs_max):
            return False

        return True

    # -----------------------------------------

    def _passes_cluster(self, cl):

        dl = cl.get("Cluster_DistLong")
        dt = cl.get("Cluster_DistLat")
        rcs = cl.get("Cluster_RCS")

        if not self._in_range(dl, self.dist_long_min, self.dist_long_max):
            return False

        if not self._in_range(dt, self.dist_lat_min, self.dist_lat_max):
            return False

        if not self._in_range(rcs, self.rcs_min, self.rcs_max):
            return False

        return True

    # -----------------------------------------

    def _in_range(self, value, vmin, vmax):

        if value is None:
            return True

        if vmin is not None and value < vmin:
            return False

        if vmax is not None and value > vmax:
            return False

        return True