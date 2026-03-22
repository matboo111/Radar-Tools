from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout,
    QDoubleSpinBox, QCheckBox
)


class NumericFilterPanel(QWidget):

    def __init__(self, object_cache, cluster_cache):
        super().__init__()

        self.object_cache = object_cache
        self.cluster_cache = cluster_cache

        layout = QVBoxLayout(self)

        self.enable_cb = QCheckBox("Enable Filters")
        layout.addWidget(self.enable_cb)

        form = QFormLayout()
        layout.addLayout(form)

        self.dl_min = QDoubleSpinBox()
        self.dl_max = QDoubleSpinBox()
        self.dt_min = QDoubleSpinBox()
        self.dt_max = QDoubleSpinBox()
        self.rcs_min = QDoubleSpinBox()
        self.rcs_max = QDoubleSpinBox()
        self.prob_min = QDoubleSpinBox()

        form.addRow("DistLong Min", self.dl_min)
        form.addRow("DistLong Max", self.dl_max)
        form.addRow("DistLat Min", self.dt_min)
        form.addRow("DistLat Max", self.dt_max)
        form.addRow("RCS Min", self.rcs_min)
        form.addRow("RCS Max", self.rcs_max)
        form.addRow("Prob Min", self.prob_min)

        # sinais
        self.enable_cb.stateChanged.connect(self.update_filters)
        for w in [
            self.dl_min, self.dl_max,
            self.dt_min, self.dt_max,
            self.rcs_min, self.rcs_max,
            self.prob_min
        ]:
            w.valueChanged.connect(self.update_filters)

    def update_filters(self):

        enabled = self.enable_cb.isChecked()

        for cache in [self.object_cache, self.cluster_cache]:

            cache.filter.enabled = enabled

            cache.filter.dist_long_min = self._get(self.dl_min)
            cache.filter.dist_long_max = self._get(self.dl_max)

            cache.filter.dist_lat_min = self._get(self.dt_min)
            cache.filter.dist_lat_max = self._get(self.dt_max)

            cache.filter.rcs_min = self._get(self.rcs_min)
            cache.filter.rcs_max = self._get(self.rcs_max)

            cache.filter.prob_min = self._get(self.prob_min)

    def _get(self, widget):
        return widget.value() if widget.value() != 0 else None