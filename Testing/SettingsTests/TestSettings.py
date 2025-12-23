from helpers.TimerFormat import format_wall_clock_from_ms
from Main import Main
from pathlib import Path
from PySide6.QtWidgets import QApplication, QMessageBox
import sys
import unittest
from unittest.mock import patch


def _get_a_main():
    BASE_DIR = Path(__file__).resolve().parents[1]  # Testing/
    CONFIG_PATH = BASE_DIR / "conf" / "test_settings.json"

    return Main(CONFIG_PATH)


class TestSettings(unittest.TestCase):
    def setUp(self):
        self._app = QApplication.instance()
        if self._app is None:
            self._app = QApplication(sys.argv)

    def test_game_load(self):
        main = _get_a_main()

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
            self.assertEqual(format_wall_clock_from_ms(game_split.pb_time_ms), widget_split.time_label.text())

            self.assertEqual(widget_split.current_time_ms, 0)
            self.assertEqual(widget_split.current_segment_ms, 0)
            self.assertEqual(widget_split.current_start_time, 0)

            self.assertEqual(game_split, widget_split.split)

        # cleanup main properly by calling its close methods, and patching out the Dialog popup
        with patch.object(QMessageBox, "exec", return_value=QMessageBox.No):  # patch out the popup
            main.close()
            main.deleteLater()

    def test_game_settings_update(self):
        main = _get_a_main()

        settings = main.settings
        game = settings.game

        game_settings = main.settings_window.tab_dict['Splits']
        game_settings.title_input.setText('TEST')
        game_settings.sub_title_input.setText('TEST')

        for i in range(game_settings.split_area.count()):
            curr_split_edit = game_settings.split_area.itemAt(i).widget()

            curr_split_edit.split_name_input.setText(curr_split_edit.split_name_input.text() + '_TEST')

        game_settings.apply()

        # make assertions about the game
        title = main.title

        self.assertEqual(game.title, 'TEST')
        self.assertEqual(title.title_label.text(), 'TEST')

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
            self.assertIn('_TEST', game_split.split_name)

            self.assertEqual(format_wall_clock_from_ms(game_split.pb_time_ms), widget_split.time_label.text())

            self.assertEqual(widget_split.current_time_ms, 0)
            self.assertEqual(widget_split.current_segment_ms, 0)
            self.assertEqual(widget_split.current_start_time, 0)

            self.assertEqual(game_split, widget_split.split)

        # cleanup main properly by calling its close methods, and patching out the Dialog popup
        with patch.object(QMessageBox, "exec", return_value=QMessageBox.No):  # patch out the popup
            main.close()
            main.deleteLater()

    def test_basic_color_settings(self):
        main = _get_a_main()
        settings = main.settings
        basic_settings = main.settings_window.tab_dict['Settings']
        color_group = basic_settings.color_group

        # setup
        color_group.backgroundColorPicker.set_color('#ffffffff')
        color_group.separatorColorPicker.set_color('#ffffffff')
        color_group.splitBackgroundColorPicker.set_color('#ffffffff')
        color_group.currentSplitBackgroundColorPicker.set_color('#ffffffff')
        color_group.bestTimeAheadPicker.set_color('#ffffffff')
        color_group.bestTimeBehindPicker.set_color('#ffffffff')
        color_group.savedTimeAheadPicker.set_color('#ffffffff')
        color_group.savedTimeBehindPicker.set_color('#ffffffff')
        color_group.lostTimeAheadPicker.set_color('#ffffffff')
        color_group.lostTimeBehindPicker.set_color('#ffffffff')

        # act
        basic_settings.apply()

        # assert
        self.assertEqual(color_group.backgroundColorPicker.color_name, settings.style.variable_map['primary-background'])
        self.assertEqual(color_group.separatorColorPicker.color_name, settings.style.variable_map['border-color'])
        self.assertEqual(color_group.splitBackgroundColorPicker.color_name, settings.style.variable_map['split-background'])
        self.assertEqual(color_group.currentSplitBackgroundColorPicker.color_name, settings.style.variable_map['current-split-background'])
        self.assertEqual(color_group.bestTimeAheadPicker.color_name, settings.style.variable_map['best-time-color-ahead'])
        self.assertEqual(color_group.bestTimeBehindPicker.color_name, settings.style.variable_map['best-time-color-behind'])
        self.assertEqual(color_group.savedTimeAheadPicker.color_name, settings.style.variable_map['saved-time-color-ahead'])
        self.assertEqual(color_group.savedTimeBehindPicker.color_name, settings.style.variable_map['saved-time-color-behind'])
        self.assertEqual(color_group.lostTimeAheadPicker.color_name, settings.style.variable_map['lost-time-color-ahead'])
        self.assertEqual(color_group.lostTimeBehindPicker.color_name, settings.style.variable_map['lost-time-color-behind'])


        with patch.object(QMessageBox, "exec", return_value=QMessageBox.No):
            main.close()
            main.deleteLater()

    def test_basic_color_bg_image_setting(self):
        main = _get_a_main()
        settings = main.settings
        basic_settings = main.settings_window.tab_dict['Settings']
        color_group = basic_settings.color_group

        # setup
        color_group.backgroundColorPicker.set_color('#ffffffff')

        # act
        basic_settings.apply()

        # assert
        self.assertEqual(color_group.backgroundColorPicker.color_name, settings.style.variable_map['primary-background'])
        self.assertEqual(settings.style.variable_map['background-image'], 'none')

        # set the background image
        color_group.backgroundImagePicker.set_file_path = 'TEST'

        # act II
        basic_settings.apply()

        # assert again
        self.assertEqual(color_group.backgroundColorPicker.color_name, settings.style.variable_map['primary-background'])
        self.assertEqual(color_group.backgroundImagePicker.file_path, 'TEST')

        with patch.object(QMessageBox, "exec", return_value=QMessageBox.No):
            main.close()
            main.deleteLater()