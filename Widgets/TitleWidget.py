from __future__ import annotations

from PySide6.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QFrame, QSizePolicy
from Models.Game import Game


class TitleWidget(QFrame):
    def __init__(self, title: str, subtitle: str, session_attempts: int, lifetime_attempts: int):
        super().__init__()
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(5, 5, 5, 3)
        self.layout.setSpacing(2)

        self.title_label = QLabel(title, self)
        self.title_label.setObjectName('TitleLabel')

        self.subtitle_label = QLabel(subtitle, self)
        self.subtitle_label.setObjectName('SubLabel')

        self.layout.addWidget(self.title_label)

        self.attempt_counter_hbox = QHBoxLayout()

        self.session_attempts_label = QLabel(str(session_attempts), self)
        self.session_attempts_label.setObjectName('sessionAttemptsLabel')

        self.lifetime_attempts_label = QLabel(str(lifetime_attempts), self)
        self.lifetime_attempts_label.setObjectName('lifetimeAttemptsLabel')

        self.attempt_counter_hbox.addWidget(self.session_attempts_label)
        self.attempt_counter_hbox.addWidget(self.subtitle_label)
        self.attempt_counter_hbox.addWidget(self.lifetime_attempts_label)

        self.layout.addLayout(self.attempt_counter_hbox)

        self.setObjectName('TitleFrame')

        self.setLayout(self.layout)
        self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)  # sets how we would like this widget to be on the main page

    @classmethod
    def from_game(cls, game: Game) -> TitleWidget:
        """
        Builds a title widget from the game 
        Args:
            game:

        Returns:

        """
        title = game.title
        sub_title = game.sub_title
        session_attempts = game.session_attempts
        lifetime_attempts = game.lifetime_attempts

        return cls(title, sub_title, session_attempts, lifetime_attempts)

    def update(self, title: str = None, subtitle: str = None, session_attempts: int = None, lifetime_attempts: int = None):
        if title is not None:
            self.title_label.setText(title)

        if subtitle is not None:
            self.subtitle_label.setText(subtitle)

        if session_attempts is not None:
            self.session_attempts_label.setText(str(session_attempts))

        if lifetime_attempts is not None:
            self.lifetime_attempts_label.setText(str(lifetime_attempts))

    def update_from_game(self, game: Game):
        self.update(game.title, game.sub_title, game.session_attempts, game.lifetime_attempts)
