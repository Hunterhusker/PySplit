from PySide6.QtGui import QFontDatabase
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QMenu, QSizePolicy, QFrame, QScrollArea
from PySide6.QtCore import Slot, Signal, QThread, Qt
import sys
import json
from time import sleep

from Listeners.KeyboardListener import KeyboardListener, KeyPressObject
from Popups.SettingsWindow import SettingsWindow
from Timer.Timer import Timer
from Timer.TimerController import TimerController
from Widgets.SplitsWidget import SplitsWidget
from Widgets.TimeStatsWidget import TimeStatsWidget
from Widgets.TimerWidget import TimerWidget
from Widgets.TitleWidget import TitleWidget
from Configurator.Configurator import Configurator


class Main(QWidget):
    StopTimer = Signal()
    StartTimer = Signal()
    PauseTimer = Signal()
    ResumeTimer = Signal()
    ReadTimer = Signal()

    Quit = Signal()
    SaveSettings = Signal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle('PySplit v0.0')

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.Title = TitleWidget('Game', 'SubTitle')
        self.Title.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)  # allows title to expand in the x (no shrinking) and leaves the y fixed

        self.MainTimerWidget = TimerWidget()

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
        self.configurator = Configurator('conf/settings.json')

        # use the configurations from the file
        self.configurator.ConfigureStyle.connect(self.set_style)

        self.splits = SplitsWidget('')
        self.splitStats = TimeStatsWidget()

        layout.addWidget(self.Title)
        layout.addWidget(self.splits)
        layout.addWidget(self.MainTimerWidget)
        layout.addWidget(self.splitStats)

        self.setLayout(layout)
        self.setGeometry(800, 800, 225, 200)

        # create a keyboard listener
        self.keyboard_listener = KeyboardListener()

        # start the keyboard listener, it already runs the listener on its own thread so there is no need to add another thread
        self.keyboard_listener.run()

        # create and connect to the timer thread
        self.game_timer = Timer()
        self.game_timer_thread = QThread()
        self.game_timer.moveToThread(self.game_timer_thread)

        # connect the game timer signals to the desired slots
        self.game_timer.update.connect(self.MainTimerWidget.update_time)
        self.game_timer.update.connect(self.splits.update_split)
        self.game_timer_thread.started.connect(self.game_timer.run)
        self.game_timer_thread.destroyed.connect(self.game_timer.stop_timer)

        self.game_timer_thread.start()

        # create the timer controller from the config
        self.timer_controller = TimerController(Listeners=[self.keyboard_listener], event_map=self.configurator.settings['inputs'])

        # connect the timer controller to the timer
        self.timer_controller.ControlEvent.connect(self.game_timer.handle_control)
        self.timer_controller.ControlEvent.connect(self.splits.handle_control)

        # also connect the extra control events from the splits to the timer
        self.splits.SplitFinish.connect(self.game_timer.stop_timer)
        self.splits.SplitReset.connect(self.game_timer.reset_timer)

        # connect up the closing signals to the closing slots
        self.Quit.connect(self.game_timer.quit)
        self.Quit.connect(self.keyboard_listener.quit)

    def contextMenuEvent(self, event):
        self.context_menu.exec(event.globalPos())

    def open_settings_popup(self):
        """
        Opens the keybinding assignment dialog popup and lets you reassign any key
        """
        dialog = SettingsWindow(self)
        dialog.setGeometry(900, 900, 600, 300)

        # lock the splitter
        self.timer_controller.listening = False

        clickedOk = dialog.exec()  # open the popup and wait for it to close

        if clickedOk:
            # give the controller the new mapping
            self.timer_controller.update_mapping(dialog.keyWidget.event_map)

            tmp = json.dumps(self.timer_controller.export_mapping(), indent=4)

        # unlock the splitter
        self.timer_controller.listening = True

    def lock_action(self, checked: bool):
        self.timer_controller.toggle_listening()

        if checked:
            self.lock_timer_action.setText('Unlock')

        else:
            self.lock_timer_action.setText('Lock')

    @Slot(str)
    def set_style(self, style):
        """
        Sets the global stylesheet for the application

        Args:
            style: (str) the style sheet data, probably read from file
        """
        self.setStyleSheet(style)

    def get_style(self):
        """
        Gets the current global stylesheet so that we can read it in and edit it as we need

        Returns:
            (str): The stylesheet data that the app is currently using
        """
        return self.styleSheet()

    def closeEvent(self, event):
        # emit a close so the threads clean up themselves
        self.Quit.emit()  # emit a quit signal
        sleep(0.125)  # wait for the quits to go through, not my proudest work, but it works

        # stop the timer thread
        self.game_timer_thread.quit()
        self.game_timer_thread.wait()

        # save the configurations to their files
        #self.configurator.write_settings()

        # accept the close event and actually close
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = Main()
    # window.setWindowFlags(Qt.FramelessWindowHint)  # uncomment this to make the top bar hide, but then you can't

    # use main's style configurations to get the initial stylesheet
    style = window.configurator.style.formatted_style_sheet
    app.setStyleSheet(style)

    window.show()

    sys.exit(app.exec())
