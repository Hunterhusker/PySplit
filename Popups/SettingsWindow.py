from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QDialog, QDialogButtonBox, QPushButton, QMessageBox, QFrame, QWidget, QTabWidget
from PySide6.QtCharts import QLineSeries, QChart, QChartView
import numpy
from PySide6.QtCore import Slot, Signal, Qt, QPointF


class SettingsWindow(QDialog):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        tabs = QTabWidget()
        tabs.addTab(TempWidget("One"), "Tab1")
        tabs.addTab(TempWidget("Two"), "Tab2")
        tabs.addTab(TempXYWidget(), "Tab3")

        # store the tabs for later
        self.tabs = tabs

        self.layout = QHBoxLayout()

        self.layout.addWidget(self.tabs)

        self.setLayout(self.layout)
        self.setWindowTitle('Settings')


class TempWidget(QWidget):
    def __init__(self, text: str = '', parent: QWidget = None):
        super().__init__(parent)
        self.layout = QVBoxLayout()

        self.lbl = QLabel(text, self)

        self.layout.addWidget(self.lbl)

        self.setLayout(self.layout)


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
