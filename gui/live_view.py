from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem

class LiveViewObject(QTableWidget):
    def __init__(self):
        super().__init__(0, 14)
        self.setHorizontalHeaderLabels(
            ["Obj_ID","RCS","DynProp,","MeasState","Class","DistLong","DistLong_rms", "DistLat","DistLat_rms", "VrelLong", "VrelLat", "Class", "Width","Length"]
        )

    def update_table_bulk(self, objects):
        self.setRowCount(0)

        for row, (oid, data) in enumerate(sorted(objects.items())):
            self.insertRow(row)

            self.setItem(row, 0, QTableWidgetItem(str(data.get("Obj_ID", ""))))
            self.setItem(row, 1, QTableWidgetItem(str(data.get("Obj_RCS", ""))))
            self.setItem(row, 2, QTableWidgetItem(str(data.get("Obj_DynProp", ""))))
            self.setItem(row, 3, QTableWidgetItem(str(data.get("Obj_MeasState", ""))))
            self.setItem(row, 4, QTableWidgetItem(str(data.get("Obj_Class", ""))))
            self.setItem(row, 5, QTableWidgetItem(str(data.get("Obj_DistLong", ""))))
            self.setItem(row, 6, QTableWidgetItem(str(data.get("Obj_DistLong_rms", ""))))
            self.setItem(row, 7, QTableWidgetItem(str(data.get("Obj_DistLat", ""))))
            self.setItem(row, 8, QTableWidgetItem(str(data.get("Obj_DistLat_rms", ""))))
            self.setItem(row, 9, QTableWidgetItem(str(data.get("Obj_VrelLong", ""))))
            self.setItem(row, 10, QTableWidgetItem(str(data.get("Obj_VrelLat", ""))))
            self.setItem(row, 11, QTableWidgetItem(str(data.get("Obj_Class", ""))))
            self.setItem(row, 12, QTableWidgetItem(str(data.get("Obj_Width", ""))))
            self.setItem(row, 13, QTableWidgetItem(str(data.get("Obj_Length", ""))))

class LiveViewCluster(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        self.table = QTableWidget()
        layout.addWidget(self.table)

        self.headers = [
            "Cluster_ID",
            "DistLong",
            "DistLat",
            "VrelLong",
            "RCS"
        ]

        self.table.setColumnCount(len(self.headers))
        self.table.setHorizontalHeaderLabels(self.headers)

    # -----------------------------------------

    def update_table_bulk(self, clusters):

        self.table.setRowCount(len(clusters))

        for row, cluster in enumerate(clusters.values()):

            self._set_item(row, 0, cluster.get("Cluster_ID"))
            self._set_item(row, 1, cluster.get("Cluster_DistLong"))
            self._set_item(row, 2, cluster.get("Cluster_DistLat"))
            self._set_item(row, 3, cluster.get("Cluster_VrelLong"))
            self._set_item(row, 4, cluster.get("Cluster_RCS"))

    # -----------------------------------------

    def _set_item(self, row, col, value):
        item = QTableWidgetItem(str(value) if value is not None else "")
        self.table.setItem(row, col, item)