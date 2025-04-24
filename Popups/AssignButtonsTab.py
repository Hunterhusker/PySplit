from PySide6.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox, QFrame, QWidget, QScrollArea
from PySide6.QtCore import Slot, Signal, Qt
import copy

from Listeners.KeyboardListener import key_to_str

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Main import Main


class AssignButtonsTab(QWidget):
    """
    A custom dialog box that we will use the remap the keys and buttons to control the splitter
    """
    def __init__(self, mainWindow: 'Main', parent: QWidget = None):
        super().__init__(parent)

        # basic window setup
        # self.setWindowTitle('Assign Hotkeys!')
        self.layout = QVBoxLayout()

        self.scrollWidget = QWidget()
        self.scrollWidgetLayout = QVBoxLayout()
        self.scrollWidgetLayout.setSpacing(3)
        self.scrollWidgetLayout.setContentsMargins(0, 0, 0, 0)

        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setFrameStyle(QFrame.NoFrame)
        self.scrollArea.setViewportMargins(0, 0, 5, 0)

        self.event_map = copy.deepcopy(mainWindow.timer_controller.get_mapping())  # save a copy of the event map

        # get the listener from the main page so we can listen to it
        self.listener = mainWindow.keyboard_listener

        # pull apart the event mapping, so I can build my assignment GUI
        keys = list(self.event_map.keys())
        values = list(self.event_map.values())

        # create the button assignment widgets
        self.assignStartSplit = KeyReassignmentLine(listener=self.listener, event_object=keys[values.index('STARTSPLIT')], timer_event='STARTSPLIT', label='Start\\Split:')
        self.assignUnsplit = KeyReassignmentLine(listener=self.listener, event_object=keys[values.index('UNSPLIT')], timer_event='UNSPLIT', label='Un-Split:')
        self.assignPause = KeyReassignmentLine(listener=self.listener, event_object=keys[values.index('PAUSE')], timer_event='PAUSE', label='Pause:')
        self.assignResume = KeyReassignmentLine(listener=self.listener, event_object=keys[values.index('RESUME')], timer_event='RESUME', label='Resume:')
        self.assignReset = KeyReassignmentLine(listener=self.listener, event_object=keys[values.index('RESET')], timer_event='RESET', label='Reset:')
        self.assignStop = KeyReassignmentLine(listener=self.listener, event_object=keys[values.index('STOP')], timer_event='STOP', label='Stop:')
        self.assignSkipSplit = KeyReassignmentLine(listener=self.listener, event_object=keys[values.index('SKIP')], timer_event='SKIP', label='Skip Split:')
        self.assignLock = KeyReassignmentLine(listener=self.listener, event_object=keys[values.index('LOCK')], timer_event='LOCK', label='Lock:')

        # also save a copy of the widgets so we can reference them by their event
        self.widgets = {
            'PAUSE': self.assignPause,
            'RESUME': self.assignResume,
            'RESET': self.assignReset,
            'STARTSPLIT': self.assignStartSplit,
            'SKIP': self.assignSkipSplit,
            'UNSPLIT': self.assignUnsplit,
            'STOP': self.assignStop,
            'LOCK': self.assignLock
        }

        self.scrollWidgetLayout.addWidget(self.assignStartSplit)
        self.scrollWidgetLayout.addWidget(self.assignUnsplit)
        self.scrollWidgetLayout.addWidget(self.assignPause)
        self.scrollWidgetLayout.addWidget(self.assignResume)
        self.scrollWidgetLayout.addWidget(self.assignStop)
        self.scrollWidgetLayout.addWidget(self.assignReset)
        self.scrollWidgetLayout.addWidget(self.assignSkipSplit)
        self.scrollWidgetLayout.addWidget(self.assignLock)

        # add a stretch to keep stuff sized right
        self.scrollWidgetLayout.addStretch()

        self.scrollWidget.setLayout(self.scrollWidgetLayout)
        self.scrollArea.setWidget(self.scrollWidget)

        self.scrollWidget.setLayout(self.scrollWidgetLayout)
        self.layout.addWidget(self.scrollArea)

        # link it all up so that this displays
        self.setLayout(self.layout)
        self.layout.setSpacing(3)

        # connect up our slots to their signals
        self.assignPause.key_assign.connect(self.assign_mapping)
        self.assignResume.key_assign.connect(self.assign_mapping)
        self.assignReset.key_assign.connect(self.assign_mapping)
        self.assignStartSplit.key_assign.connect(self.assign_mapping)
        self.assignSkipSplit.key_assign.connect(self.assign_mapping)
        self.assignUnsplit.key_assign.connect(self.assign_mapping)
        self.assignStop.key_assign.connect(self.assign_mapping)
        self.assignLock.key_assign.connect(self.assign_mapping)

    @Slot(object, str)
    def assign_mapping(self, key, timer_event):
        keys = list(self.event_map.keys())
        values = list(self.event_map.values())

        if key not in self.event_map:  # if the pressed object hasn't already been assigned
            if timer_event in values:
                idx = values.index(timer_event)  # find the loc of the old event
                keys[idx] = key  # overwrite the mapping

            else:
                keys.append(key)
                values.append(timer_event)

        else:
            # find what this should be and set it back
            idx = values.index(timer_event)

            old_key = keys[idx]

            widget = self.widgets[timer_event]  # find the widget that gave this event

            widget.assign_key(old_key)

            dlg = QMessageBox(self)
            dlg.setWindowTitle("Reassignment Failed!")
            dlg.setText("That key is already in use!")
            dlg.exec()

        self.event_map = dict(zip(keys, values))  # remake the map and set it


class KeyReassignmentLine(QFrame):
    """
    A single key reassignment widget to use multiple instances of to update the input mapping with
    """
    listening = False
    key_assign = Signal(object, str)

    def __init__(self, listener, event_object, timer_event: str, label: str = None):
        super().__init__()

        # set the instance variables of this obj
        self.listener = listener
        self.event_object = event_object
        self.timer_event = timer_event

        self.setFixedHeight(35)

        if hasattr(event_object, 'value'):
            self.key_str = event_object.value
        else:
            self.key_str = '...'

        self.line_layout = QHBoxLayout()

        # create and style the label
        if label is None:
            label = timer_event

        self.event_label = QLabel(label)
        self.event_label.setObjectName('KeyAssignmentLabel')

        # create the button
        self.triggerButton = QPushButton(self.key_str)
        self.triggerButton.setFixedSize(80, 25)

        # add the elements to the widget
        self.line_layout.addWidget(self.event_label)
        self.line_layout.addWidget(self.triggerButton)
        self.line_layout.setContentsMargins(10, 0, 10, 0)

        self.setLayout(self.line_layout)

        # align our items in the line
        self.line_layout.setAlignment(self.triggerButton, Qt.AlignRight | Qt.AlignVCenter)
        self.line_layout.setAlignment(self.event_label, Qt.AlignLeft | Qt.AlignVCenter)

        # hookup the slots and signals
        self.triggerButton.clicked.connect(self.toggle_listening)

        # name this thing so we can globally style it different from the rest
        self.setObjectName('KeyReassignmentLine')

    def assign_key(self, obj):
        self.event_object = obj
        self.key_str = key_to_str(self.event_object)

        self.triggerButton.setText(self.key_str)

    @Slot()
    def toggle_listening(self):
        if self.listening:
            self.listening = False
            self.listener.on_press.disconnect(self.listen_for_key)

            # update the label on the button too
            self.triggerButton.setText(self.key_str)
            self.triggerButton.clearFocus()  # lose the focus on this button too

        else:
            self.listening = True
            self.listener.on_press.connect(self.listen_for_key)

            self.triggerButton.setText('...')  # TODO: setup a QTimer to count down from 5 and then untoggle

    @Slot(object)
    def listen_for_key(self, event_object):
        self.event_object = event_object

        if hasattr(self.event_object, 'value'):
            self.key_str = self.event_object.value
        else:
            self.key_str = '...'

        # emit the change to the outer class
        self.key_assign.emit(self.event_object, self.timer_event)

        self.toggle_listening()  # auto-stop listening to key presses
