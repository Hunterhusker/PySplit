from PySide6.QtCharts import QLineSeries, QChart, QChartView
from PySide6.QtCore import QPointF
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QWidget, QVBoxLayout
# Just brought over some test code here that I used to mock up what this will look like when it is ready


class TempXYWidget(QWidget):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.layout = QVBoxLayout()

        series = QLineSeries()
        series.append([QPointF(0, 0), QPointF(1, 1), QPointF(2, 4), QPointF(3, 9), QPointF(4, 16)])

        chart = QChart()
        chart.addSeries(series)
        chart.createDefaultAxes()

        self.chart_view = QChartView(chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)

        self.layout.addWidget(self.chart_view)

        self.setLayout(self.layout)
