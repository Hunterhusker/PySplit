from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QDialog, QDialogButtonBox, QPushButton, QMessageBox, QFrame, QWidget, QTabWidget
from PySide6.QtCharts import QLineSeries, QChart, QChartView
from PySide6.QtCore import Slot, Signal, Qt, QPointF, QObject

from Listeners import ABCListener
from Popups.AssignButtonsDialog import AssignButtonsDialog


class SettingsWindow(QDialog):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        self.layout = QVBoxLayout()

        self.keyWidget = AssignButtonsDialog(parent.timer_controller.get_mapping(), parent.keyboard_listener)

        self.tabs = QTabWidget()
        self.tabs.addTab(TempWidget("One"), "Tab1")
        self.tabs.addTab(TempXYWidget(), "Tab2")
        self.tabs.addTab(self.keyWidget, 'Key Bindings')

        # set up our standard dialog buttons
        self.dialogButtons = QDialogButtonBox()
        #self.dialogButtons.setCenterButtons(True)

        # create buttons for the button dialog
        self.dialogButtons.addButton(QDialogButtonBox.Ok)
        self.dialogButtons.addButton(QDialogButtonBox.Apply)
        self.dialogButtons.addButton(QDialogButtonBox.Cancel)

        for button in self.dialogButtons.buttons():
            button.setFixedSize(80, 25)

        # link the buttons to what they need to do
        # self.dialogButtons.accepted.connect(self.accept)
        # self.dialogButtons.rejected.connect(self.reject)

        self.dialogButtons.clicked.connect(self.button_event)

        self.layout.addWidget(self.tabs)
        self.layout.addWidget(self.dialogButtons)

        self.setLayout(self.layout)
        self.setWindowTitle('Settings')

    def apply_settings(self):
        """
        Applies the settings to the application, since each page will know what to emit
        """
        pass

    def button_event(self, button: QPushButton):
        role = self.dialogButtons.buttonRole(button)

        if role == QDialogButtonBox.AcceptRole:
            self.apply_settings()  # apply as normal
            self.accept()  # accept the changes lol

        elif role == QDialogButtonBox.RejectRole:
            self.reject()

        elif role == QDialogButtonBox.ApplyRole:
            self.apply_settings()
            print('here is where you can add code to apply settings changes w/o closing the page!!')


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
