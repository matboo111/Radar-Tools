from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem

class LiveView(QTableWidget):
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
