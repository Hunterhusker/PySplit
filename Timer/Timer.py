from PySide6.QtCore import QElapsedTimer, QObject, QTimer, Slot, Signal


class Timer(QObject):
    update = Signal(int)

    paused = False
    running = False
    prevTime = 0

    def __init__(self):
        super().__init__()
        self.timer = None
        self.update_timer = None
        self.prevTime = 0

        # set up the function map so we can take in inputs
        self.event_map = {  # mapping is constant for now, we don't want them to remap these on the fly
            'STARTSPLIT': self.startsplit_timer,
            'UNSPLIT': self.doNothing,
            'PAUSE': self.pause_timer,
            'STOP': self.stop_timer,
            'RESET': self.reset_timer,
            'SKIP': self.doNothing,
            'RESUME': self.resume_timer,
            'LOCK': self.doNothing
        }

    def run(self):
        self.timer = QElapsedTimer()
        self.timer.start()

        self.update_timer = QTimer()
        self.update_timer.setInterval(1)
        self.update_timer.timeout.connect(self.read)

        self.update.emit(0)

    @Slot(str)
    def handle_control(self, control_message: str):
        if control_message in self.event_map:  # if the message is handleable
            self.event_map[control_message]()  # handle it according to the mapping

    def doNothing(self):
        """
        A simple method that does nothing to fill in slots in the timer that shouldn't do anything
        """
        pass

    @Slot()
    def startsplit_timer(self):
        if not self.running:
            if self.timer.isValid():
                self.timer.restart()

            else:
                self.timer.start()

            self.update_timer.start()
            self.prevTime = 0

            # manage state
            self.running = True
            self.paused = False

            self.update.emit(0)  # just started so it should be 0

    @Slot()
    def reset_timer(self):
        self.update_timer.stop()

        # manage state, not running and not paused, since a stopped timer cannot be resumed
        self.running = False
        self.paused = False
        self.prevTime = 0  # prev time of 0 so we can't resume from here

        self.update.emit(0)  # reset to 0, since the timer was stopped

    @Slot()
    def stop_timer(self):
        if self.running:  # only need to stop the timer if it is already on
            curr = self.timer.elapsed()
            self.update_timer.stop()

            # manage state, not running and not paused, since a stopped timer cannot be resumed
            self.running = False
            self.paused = False
            self.prevTime = 0  # prev time of 0 so we can't resume from here

            self.update.emit(curr)  # output the last value so it shows on the screen

    @Slot()
    def pause_timer(self):
        if not self.paused and self.running:
            curr = self.timer.elapsed()
            self.prevTime += curr  # save the curr to prev

            self.update_timer.stop()  # stop the update timer
            self.update.emit(self.prevTime)

            # manage state, a paused timer is still running, just also paused
            self.paused = True
            self.running = True

    @Slot()
    def resume_timer(self):
        if self.paused and self.running:
            self.timer.restart()
            self.update_timer.start()

            self.update.emit(self.prevTime)

            # manage state
            self.paused = False
            self.running = True

    @Slot(str)
    def read_str(self):
        curr = self.timer.elapsed() + self.prevTime

        s, ms = divmod(curr, 1000)

        self.update.emit(f'{s}.{ms}')

    @Slot(int)
    def read(self):
        """
        Returns:
            (int) The current time on the timer in milliseconds
        """
        curr = self.timer.elapsed()
        self.update.emit(curr + self.prevTime)

    @Slot()
    def quit(self):
        if self.update_timer.isActive():
            self.update_timer.stop()
