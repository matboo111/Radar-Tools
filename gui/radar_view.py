from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import pyqtgraph as pg
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from processing.radar_mode import RadarMode

class RadarView(FigureCanvas):
    # This method is used with matplotlib
    # def __init__(self):
    #     self.figure = Figure()
    #     super().__init__(self.figure)
    #     self.ax = self.figure.add_subplot(111)
    #     self.ax.set_xlabel("Distância Lateral (m)")
    #     self.ax.set_ylabel("Distância Longitudinal (m)")
    #     self.ax.set_xlim(-50, 50)
    #     self.ax.set_ylim(0, 200)

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        # Widget principal
        self.plot_widget = pg.PlotWidget()
        layout.addWidget(self.plot_widget)

        # ===== CONFIGURAÇÃO PROFISSIONAL =====

        # Fundo
        self.plot_widget.setBackground("k")

        # Grid real
        self.plot_widget.showGrid(x=True, y=True, alpha=0.3)

        # Escala igual nos dois eixos
        self.plot_widget.setAspectLocked(True)

        # Labels
        self.plot_widget.setLabel("left", "Lateral Distance (m)")
        self.plot_widget.setLabel("bottom", "Longitudinal Distance (m)")

        # Range inicial típico ARS408
        self.plot_widget.setXRange(-50, 50)
        self.plot_widget.setYRange(50, 50)

        # Ativar mouse interativo
        self.plot_widget.setMouseEnabled(x=True, y=True)

        # Melhor qualidade de renderização
        self.plot_widget.setAntialiasing(True)

        # Scatter dos objetos
        self.scatter = pg.ScatterPlotItem(
            size=10,
            brush=pg.mkBrush(0, 255, 0, 200),
            pen=pg.mkPen(None)
        )

        car = pg.RectROI([-2, -1], [4, 1], movable=False)
        self.plot_widget.addItem(car)

        self.plot_widget.addItem(self.scatter)

        self.mode = RadarMode.OBJECT

        self.visible_radars = set(range(8))

    def update_plot_bulk(self, objects):

        spots = []

        RADAR_COLORS = {
            0: (255, 0, 0),
            1: (0, 255, 0),
            2: (0, 0, 255),
            3: (255, 255, 0),
            4: (255, 0, 255),
            5: (0, 255, 255),
            6: (200, 100, 0),
            7: (100, 0, 200),
        }

        if self.mode == RadarMode.OBJECT:

            for obj in objects.values():

                rid = obj.get("Radar_ID", 0)

                if rid not in self.visible_radars:
                    continue

                x = obj.get("Obj_DistLat", 0)
                y = obj.get("Obj_DistLong", 0)

                color = RADAR_COLORS.get(rid, (255, 255, 255))

                spots.append({
                    'pos': (x, y),
                    'brush': color,
                    'size': 8
                })

        elif self.mode == RadarMode.CLUSTER:

            for cluster in objects.values():

                rid = cluster.get("Radar_ID", 0)

                if rid not in self.visible_radars:
                    continue

                x = cluster.get("Cluster_DistLat", 0)
                y = cluster.get("Cluster_DistLong", 0)

                color = RADAR_COLORS.get(rid, (255, 255, 255))

                spots.append({
                    'pos': (x, y),
                    'brush': color,
                    'size': 6
                })

        self.scatter.setData(spots)

    def set_visible_radars(self, radar_ids):
        self.visible_radars = set(radar_ids)

