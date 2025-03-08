from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QMenu, QSizePolicy, QFrame
from PySide6.QtCore import Slot, Signal, QThread
import sys
import json
from time import sleep

from Dialogs.AssignButtonsDialog import AssignButtonsDialog
from Listeners.KeyboardListener import KeyboardListener, KeyPressObject
from Timer.Timer import Timer
from Timer.TimerController import TimerController
from Widgets.SplitsWidget import SplitsWidget
from Widgets.TimerWidget import TimerWidget
from Widgets.TitleWidget import TitleWidget
from Configurator.SettingsParser import SettingsParser
from helpers.TimerFormat import format_wall_clock_from_ms


class Main(QWidget):
    StopTimer = Signal()
    StartTimer = Signal()
    PauseTimer = Signal()
    ResumeTimer = Signal()
    ReadTimer = Signal()

    Quit = Signal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle('PySplit v0.0')

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.Title = TitleWidget('Super Mario World', '11 Exit Glitchless')
        self.Title.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)  # allows title to expand in the x (no shrinking) and leaves the y fixed

        self.MainTimerWidget = TimerWidget()

        self.context_menu = QMenu(self)
        assignButtonsAction = self.context_menu.addAction('Assign Buttons')
        assignButtonsAction.triggered.connect(self.open_key_dialog)

        # load the settings from the file
        self.settings_parser = SettingsParser('settings.json')
        self.settings_parser.parse_settings()

        # Create the configurator and hook everything to it

        #self.Title.setStyleSheet(self.settings_parser.settings['style']['title'])
        self.splits = SplitsWidget()

        layout.addWidget(self.Title)
        layout.addWidget(self.splits)
        layout.addStretch()
        layout.addWidget(self.MainTimerWidget)

        self.setLayout(layout)
        self.setGeometry(800, 800, 300, 200)

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
        self.timer_controller = TimerController(Listeners=[self.keyboard_listener], event_map=self.settings_parser.settings['inputs'])

        # connect the timer controller to the timer
        self.timer_controller.ControlEvent.connect(self.game_timer.handle_control)
        self.timer_controller.ControlEvent.connect(self.splits.handle_control)

        # connect up the closing signals to the closing slots
        self.Quit.connect(self.game_timer.quit)
        self.Quit.connect(self.keyboard_listener.quit)

        self.setStyleSheet("""
            Main {
                background-color: #2b2b2b;
            }
            
            QPushButton {
                color: #a3a4ab;
                background-color: #4c5052;
                border: 2px solid #4c5052;
                border-radius: 5px;
            }
        """)

    def contextMenuEvent(self, event):
        self.context_menu.exec(event.globalPos())

    def open_key_dialog(self):
        """
        Opens the keybinding assignment dialog popup and lets you reassign any key
        """
        # get the current mapping
        event_map = self.timer_controller.get_mapping()

        dialog = AssignButtonsDialog(event_map=event_map, listener=self.keyboard_listener)
        dialog.setGeometry(900, 900, 300, 450)

        clickedOk = dialog.exec()  # open the popup and wait for it to close

        if clickedOk:
            # give the controller the new mapping
            self.timer_controller.update_mapping(dialog.event_map)

            tmp = json.dumps(self.timer_controller.export_mapping(), indent=4)

    def closeEvent(self, event):
        # emit a close so the threads clean up themselves
        self.Quit.emit()  # emit a quit signal
        sleep(0.125)  # wait for the quits to go through, not my proudest work, but it works

        # stop the timer thread
        self.game_timer_thread.quit()
        self.game_timer_thread.wait()

        # update the settings with what we set
        settings_json = {}
        inputs_json = self.timer_controller.export_mapping()

        settings_json['inputs'] = inputs_json
        settings_json['style'] = {}

        settings_json['style']['title'] = self.Title.styleSheet()

        json_str = json.dumps(settings_json, indent=4)

        with open('settings.json', 'w') as f:
            f.write(json_str)

        # accept the close event and actually close
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = Main()
    window.show()

    sys.exit(app.exec())
