import resources_rc  # imports the static SVGs

from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QMenu, QMessageBox, QMainWindow
from PySide6.QtCore import Slot, Signal, QThread, Qt, QFile
from PySide6.QtGui import QIcon
import sys

from Database.Repository import Repository
from Listeners.AggregateListener import AggregateListener
from Listeners.KeyboardListener import KeyboardListener
from Popups.AdvancedStyleTab import AdvancedStyleTab
from Popups.AssignButtonsTab import AssignButtonsTab
from Popups.BasicSettingsTab import BasicSettingsTab
from Popups.SettingsWindow import SettingsWindow
from Popups.GameSettingsTab import GameSettingsTab
from Settings.Session import Session
from Settings.Settings import Settings
from Timer.SplitTimer import SplitTimer
from Timer.Timer import Timer
from Timer.TimerController import TimerController
from Widgets.SplitsWidget import SplitsWidget
from Widgets.TimeStatsWidget import TimeStatsWidget
from Widgets.TimerWidget import TimerWidget
from Widgets.TitleWidget import TitleWidget


class Main(QWidget):
    Quit = Signal()
    SaveSettings = Signal()

    _widget_starting_location = None  # the starting location of the widget, used for click and drag actions

    def __init__(self, settings_path: str = 'conf/settings.json'):
        super().__init__()

        # Set up the window itself we can add stuff
        self.setWindowTitle('PySplit v0.0')
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window | Qt.WindowStaysOnTopHint)

        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setAutoFillBackground(True)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # establish our session object
        self.session = Session(settings_path)

        # Create the widgets
        self.title = TitleWidget.from_game(self.session.game)
        self.split_timer = SplitTimer(self.session)
        self.splits = SplitsWidget(self.session, self.split_timer, parent=self)
        self.main_timer_widget = TimerWidget(self.split_timer)
        self.splitStats = TimeStatsWidget()

        # connect widgets to the events they care of
        self.session.settings.style.UpdateStyle.connect(self.set_style)
        self.session.settings.SettingsUpdate.connect(self.splits.apply_settings)
        self.split_timer.SplitUpdate.connect(self.splits.update_split)

        # create our right click menu
        self.context_menu = QMenu(self)
        self.settings_action = self.context_menu.addAction('Settings')
        self.settings_action.triggered.connect(self.open_settings_popup)

        self.lock_timer_action = self.context_menu.addAction('Lock')
        self.lock_timer_action.setCheckable(True)
        self.lock_timer_action.setChecked(False)
        self.lock_timer_action.toggled.connect(self.lock_action)

        self.exit_action = self.context_menu.addAction('Exit')
        self.exit_action.triggered.connect(QApplication.instance().quit)

        # Add our parts to the page itself
        layout.addWidget(self.title)
        layout.addWidget(self.splits)
        layout.addWidget(self.main_timer_widget)
        layout.addWidget(self.splitStats)

        self.setLayout(layout)
        self.setGeometry(800, 800, 225, 200)

        # create and connect to the timer thread
        self.game_timer = Timer(self.session)
        self.game_timer_thread = QThread()
        self.game_timer.moveToThread(self.game_timer_thread)
        self.session.game.GameUpdated.connect(self.game_timer.sync_timer_settings)

        # connect the game timer signals to the desired slots
        self.game_timer.tick.connect(self.split_timer.on_tick)
        self.game_timer_thread.started.connect(self.game_timer.run)
        self.game_timer_thread.destroyed.connect(self.game_timer.stop_timer)

        self.game_timer_thread.start()

        aggregate_listener = AggregateListener(listeners=[KeyboardListener()])

        # create the timer controller from the config
        self.timer_controller = TimerController(listener=aggregate_listener, session=self.session)

        # connect the timer controller to the timer
        self.timer_controller.ControlEvent.connect(self.game_timer.handle_control)
        self.timer_controller.ControlEvent.connect(self.split_timer.handle_control)

        # also connect the extra control events from the splits to the timer
        self.split_timer.SplitsFinish.connect(self.game_timer.stop_timer)
        #self.split_timer.SplitsFinish.connect(self.settings._repository.save_run)  # TODO : need to figure out how and what to pass in here
        self.split_timer.SplitsFinish.connect(self.session.repository.open_save_dialog)

        self.split_timer.SplitsReset.connect(self.game_timer.reset_timer)

        self.session.game.GameUpdated.connect(self.splits.load_splits_from_game)
        self.session.game.GameUpdated.connect(self.split_timer.reset)
        self.session.game.GameUpdated.connect(self.title.update_from_game)

        self.settings_window = SettingsWindow(parent=self)
        self.settings_window.setGeometry(900, 900, 600, 400)
        self.settings_window.setMinimumSize(600, 400)
        self.settings_window.add_tab(AssignButtonsTab(self.session, timer_controller=self.timer_controller, parent=self.settings_window), 'Key Bindings')
        self.settings_window.add_tab(GameSettingsTab(self.session, parent=self.settings_window), 'Splits')
        self.settings_window.add_tab(BasicSettingsTab(self.session, parent=self.settings_window), 'Settings')
        self.settings_window.add_tab(AdvancedStyleTab(self.session, parent=self.settings_window), 'Advanced')

        self.settings_window.toggle_tab_visibility('Advanced')

        self.setObjectName('MainWindow')

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
        # stop listening to events
        self.timer_controller.toggle_listening()

        # make a popup to ask the user if they would like to save changes before exiting
        save_box = QMessageBox(self)
        save_box.setWindowTitle('Save Changes?')
        save_box.setText('Would you like to save any configuration changes and new PBs?')
        save_box.setStandardButtons(QMessageBox.StandardButton.No | QMessageBox.StandardButton.Yes)
        save_box.setIcon(QMessageBox.Icon.Question)

        # resize the buttons
        save_no = save_box.button(QMessageBox.StandardButton.No)
        save_no.setMinimumSize(75, 25)

        save_yes = save_box.button(QMessageBox.StandardButton.Yes)
        save_yes.setMinimumSize(75, 25)

        result = save_box.exec()

        if result == QMessageBox.StandardButton.Yes:
            self.session.repository.save_game(self.session.game)
            self.session.settings.save_settings()
            #self.settings.game.to_json_file(self.settings.settings['game_path'])

        self.Quit.emit()  # provide a Quit event to notify the system we are quitting

        # stop our non-thread objects
        self.game_timer.quit()
        self.timer_controller.stop_listening()

        # stop thhreads
        self.game_timer_thread.quit()
        self.game_timer_thread.wait()

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
    icon = QIcon(':icons/Static/pysplitIcon.png')

    window = Main()

    # set the window's icon
    window.setWindowIcon(icon)

    # use main's style configurations to get the initial stylesheet
    style = window.session.settings.style.formatted_style_sheet
    app.setStyleSheet(style)

    window.show()

    sys.exit(app.exec())
