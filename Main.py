from PySide6.QtGui import QFontDatabase
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QMenu, QSizePolicy, QFrame, QScrollArea
from PySide6.QtCore import Slot, Signal, QThread, Qt
import sys
import json
from time import sleep

from Listeners.AggregateListener import AggregateListener
from Listeners.KeyboardListener import KeyboardListener
from Models.Game import Game
from Popups.AssignButtonsTab import AssignButtonsTab
from Popups.SettingsWindow import SettingsWindow
from Popups.SplitsTab import SplitsTab
from Popups.StyleTab import StyleTab
from Timer.Timer import Timer
from Timer.TimerController import TimerController
from Widgets.SplitsWidget import SplitsWidget
from Widgets.TimeStatsWidget import TimeStatsWidget
from Widgets.TimerWidget import TimerWidget
from Widgets.TitleWidget import TitleWidget
from Styling.Configurator import Configurator


class Main(QWidget):
    StopTimer = Signal()
    StartTimer = Signal()
    PauseTimer = Signal()
    ResumeTimer = Signal()
    ReadTimer = Signal()

    Quit = Signal()
    SaveSettings = Signal()

    _widget_starting_location = None  # the starting location of the widget, used for click and drag actions

    def __init__(self):
        super().__init__()
        self.setWindowTitle('PySplit v0.0')
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.game = Game.from_json_file('conf/testGame.json')

        self.title = TitleWidget.from_game(self.game)

        self.main_timer_widget = TimerWidget()

        self.context_menu = QMenu(self)

        self.settings_action = self.context_menu.addAction('Settings')
        self.settings_action.triggered.connect(self.open_settings_popup)

        self.lock_timer_action = self.context_menu.addAction('Lock')
        self.lock_timer_action.setCheckable(True)
        self.lock_timer_action.setChecked(False)
        self.lock_timer_action.toggled.connect(self.lock_action)

        self.exit_action = self.context_menu.addAction('Exit')
        self.exit_action.triggered.connect(QApplication.instance().quit)

        # load the settings from the file
        self.configurator = Configurator('conf/settings.json', 'conf/testGame.json')

        # use the configurations from the file
        self.configurator.style.UpdateStyle.connect(self.set_style)

        self.splits = SplitsWidget(self.game)
        self.splitStats = TimeStatsWidget()

        layout.addWidget(self.title)
        layout.addWidget(self.splits)
        layout.addWidget(self.main_timer_widget)
        layout.addWidget(self.splitStats)

        self.setLayout(layout)
        self.setGeometry(800, 800, 225, 200)

        # create and connect to the timer thread
        self.game_timer = Timer()
        self.game_timer_thread = QThread()
        self.game_timer.moveToThread(self.game_timer_thread)

        # connect the game timer signals to the desired slots
        self.game_timer.update.connect(self.main_timer_widget.update_time)
        self.game_timer.update.connect(self.splits.update_split)
        self.game_timer_thread.started.connect(self.game_timer.run)
        self.game_timer_thread.destroyed.connect(self.game_timer.stop_timer)

        self.game_timer_thread.start()

        aggregate_listener = AggregateListener(listeners=[KeyboardListener()])

        # create the timer controller from the config
        self.timer_controller = TimerController(listener=aggregate_listener, event_map=self.configurator.settings['inputs'])

        # connect the timer controller to the timer
        self.timer_controller.ControlEvent.connect(self.game_timer.handle_control)
        self.timer_controller.ControlEvent.connect(self.splits.handle_control)

        # also connect the extra control events from the splits to the timer
        self.splits.SplitFinish.connect(self.game_timer.stop_timer)
        self.splits.SplitReset.connect(self.game_timer.reset_timer)

        self.settings_window = SettingsWindow(parent=self)
        self.settings_window.setGeometry(900, 900, 400, 400)
        self.settings_window.add_tab(StyleTab(mainWindow=self), 'Style')
        self.settings_window.add_tab(AssignButtonsTab(mainWindow=self), 'Key Bindings')
        self.settings_window.add_tab(SplitsTab(mainWindow=self), 'Splits')

        # connect up the closing signals to the closing slots
        self.Quit.connect(self.game_timer.quit)
        self.Quit.connect(self.timer_controller.listener.quit)

    def contextMenuEvent(self, event):
        if not self.game_timer.running:  # only open if the timer is not running, don't play with settings! PLAY THE GAME!
            self.context_menu.exec(event.globalPos())

    def open_settings_popup(self):
        """
        Opens the keybinding assignment dialog popup and lets you reassign any key
        """
        # lock the splitter
        self.timer_controller.listening = False

        self.settings_window.exec()  # open the popup and wait for it to close

        # unlock the splitter
        self.timer_controller.listening = True

    def lock_action(self, checked: bool):
        self.timer_controller.toggle_listening()

        if checked:
            self.lock_timer_action.setText('Unlock')

        else:
            self.lock_timer_action.setText('Lock')

        self.context_menu.show()  # try and keep the menu open

    @Slot(str)
    def set_style(self, stylesheet):
        """
        Sets the global stylesheet for the application

        Args:
            stylesheet: (str) the style sheet data, probably read from file
        """
        self.setStyleSheet(stylesheet)

    def get_style(self):
        """
        Gets the current global stylesheet so that we can read it in and edit it as we need

        Returns:
            (str): The stylesheet data that the app is currently using
        """
        return self.styleSheet()

    def closeEvent(self, event):
        # emit a close so the threads clean themselves up
        self.Quit.emit()  # emit a quit signal
        sleep(0.125)  # wait for the quits to go through, not my proudest work, but it works

        # stop the timer thread
        self.game_timer_thread.quit()
        self.game_timer_thread.wait()

        # save the configurations to their files
        #self.configurator.write_settings()

        # accept the close event and actually close
        event.accept()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._widget_starting_location = event.globalPosition().toPoint() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if self._widget_starting_location is not None and event.buttons() & Qt.LeftButton:
            self.move(event.globalPosition().toPoint() - self._widget_starting_location)

    def mouseReleaseEvent(self, event):
        self._widget_starting_location = None


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = Main()

    # use main's style configurations to get the initial stylesheet
    style = window.configurator.style.formatted_style_sheet
    app.setStyleSheet(style)

    window.show()

    sys.exit(app.exec())
