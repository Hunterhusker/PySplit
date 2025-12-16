import unittest
from unittest.mock import patch
from PySide6.QtWidgets import QApplication, QMessageBox
from Main import Main


class TestSettings(unittest.TestCase):
    def test_game_load(self):
        app = QApplication([])  # it says unused, but it needs to be made before we can make Main
        main = Main('Testing/conf/test_settings.json')

        settings = main.settings
        game = settings.game

        # make assertions about the game
        title = main.title

        self.assertEqual(game.title, title.title_label.text())
        self.assertEqual(game.sub_title, title.subtitle_label.text())
        self.assertEqual(str(game.session_attempts), title.session_attempts_label.text())
        self.assertEqual(str(game.lifetime_attempts), title.lifetime_attempts_label.text())

        splits_widget = main.splits.splits
        game_splits = game.splits

        self.assertEqual(len(game_splits), len(splits_widget))

        for i in range(len(game_splits)):
            game_split = game_splits[i]
            widget_split = splits_widget[i]

            self.assertEqual(game_split.split_name, widget_split.split_name_label.text())

        # cleanup main properly by calling its close methods, and patching out the Dialog popup
        with patch.object(QMessageBox, "exec", return_value=QMessageBox.No):  # patch out the popup
            main.close()
            main.deleteLater()
