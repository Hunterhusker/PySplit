from helpers.TimerFormat import format_wall_clock_from_ms
from Main import Main
from pathlib import Path
from PySide6.QtGui import QFontDatabase, QColor
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

        self.main = _get_a_main()

    def tearDown(self):
        if self.main is not None:
            with patch.object(QMessageBox, "exec", return_value=QMessageBox.No):  # patch out the popup
                self.main.close()
                self.main.deleteLater()


    def test_game_load(self):
        settings = self.main.settings
        game = settings.game

        # make assertions about the game
        title = self.main.title

        self.assertEqual(game.title, title.title_label.text())
        self.assertEqual(game.sub_title, title.subtitle_label.text())
        self.assertEqual(str(game.session_attempts), title.session_attempts_label.text())
        self.assertEqual(str(game.lifetime_attempts), title.lifetime_attempts_label.text())

        splits_widget = self.main.splits.splits
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

    def test_game_settings_update(self):
        settings = self.main.settings
        game = settings.game

        game_settings = self.main.settings_window.tab_dict['Splits']
        game_settings.title_input.setText('TEST')
        game_settings.sub_title_input.setText('TEST')

        for i in range(game_settings.split_area.count()):
            curr_split_edit = game_settings.split_area.itemAt(i).widget()

            curr_split_edit.split_name_input.setText(curr_split_edit.split_name_input.text() + '_TEST')

        game_settings.apply()

        # make assertions about the game
        title = self.main.title

        self.assertEqual(game.title, 'TEST')
        self.assertEqual(title.title_label.text(), 'TEST')

        self.assertEqual(game.sub_title, title.subtitle_label.text())
        self.assertEqual(str(game.session_attempts), title.session_attempts_label.text())
        self.assertEqual(str(game.lifetime_attempts), title.lifetime_attempts_label.text())

        splits_widget = self.main.splits.splits
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

    def test_basic_color_settings(self):
        settings = self.main.settings
        basic_settings = self.main.settings_window.tab_dict['Settings']
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

    def test_basic_color_bg_image_setting(self):
        settings = self.main.settings
        basic_settings = self.main.settings_window.tab_dict['Settings']
        color_group = basic_settings.color_group

        # setup
        color_group.backgroundColorPicker.set_color('#ffffffff')

        # act
        color_group.apply()

        # assert
        self.assertEqual(color_group.backgroundColorPicker.color_name, settings.style.variable_map['primary-background'])
        self.assertEqual(settings.style.variable_map['background-image'], 'none')

        # set the background image
        color_group.backgroundImagePicker.set_file_path('TEST')

        # act II
        basic_settings.apply()

        # assert again
        self.assertEqual(color_group.backgroundColorPicker.color_name, settings.style.variable_map['primary-background'])
        self.assertEqual(color_group.backgroundImagePicker.file_path, 'TEST')
        self.assertEqual(settings.style.variable_map['background-image'], 'url("TEST") 0 0 0 0 stretch stretch')

    def test_basic_text_setting_update_font(self):
        settings = self.main.settings
        var_map = settings.style.variable_map

        basic_settings = self.main.settings_window.tab_dict['Settings']
        text_settings = basic_settings.text_group
        font_families = QFontDatabase.families()

        # setup
        og_title_family = text_settings.title_font_picker.get_font_family()
        og_subtitle_family = text_settings.subtitle_font_picker.get_font_family()
        og_attempts_family = text_settings.attempts_font_picker.get_font_family()
        og_split_family = text_settings.split_font_picker.get_font_family()
        og_timer_family = text_settings.timer_font_picker.get_font_family()

        og_title_family_idx = font_families.index(og_title_family)
        og_subtitle_family_idx = font_families.index(og_subtitle_family)
        og_attempts_family_idx = font_families.index(og_attempts_family)
        og_split_family_idx = font_families.index(og_split_family)
        og_timer_family_idx = font_families.index(og_timer_family)

        # will break if there are less than like 25 fonts on a system but that probably won't happen
        new_title_family_idx = max(og_title_family_idx - 10, 0) if og_title_family_idx >= 0 else max(og_title_family_idx + 10, 0)
        new_subtitle_family_idx = max(og_subtitle_family_idx - 10, 0) if og_subtitle_family_idx >= 0 else max(og_subtitle_family_idx + 10, 0)
        new_attempts_family_idx = max(og_attempts_family_idx - 10, 0) if og_attempts_family_idx >= 0 else max(og_attempts_family_idx + 10, 0)
        new_split_family_idx = max(og_split_family_idx - 10, 0) if og_split_family_idx >= 0 else max(og_split_family_idx + 10, 0)
        new_timer_family_idx = max(og_timer_family_idx - 10, 0) if og_timer_family_idx >- 0 else max(og_timer_family_idx + 10, 0)

        new_title_family = font_families[new_title_family_idx]
        new_subtitle_family = font_families[new_subtitle_family_idx]
        new_attempts_family = font_families[new_attempts_family_idx]
        new_split_family = font_families[new_split_family_idx]
        new_timer_family = font_families[new_timer_family_idx]

        # act
        text_settings.title_font_picker.set_font_family(new_title_family)
        text_settings.subtitle_font_picker.set_font_family(new_subtitle_family)
        text_settings.attempts_font_picker.set_font_family(new_attempts_family)
        text_settings.split_font_picker.set_font_family(new_split_family)
        text_settings.timer_font_picker.set_font_family(new_timer_family)

        text_settings.apply()

        # assert
        self.assertNotEqual(og_title_family, new_title_family)
        self.assertNotEqual(og_subtitle_family, new_subtitle_family)
        self.assertNotEqual(og_attempts_family, new_attempts_family)
        self.assertNotEqual(og_split_family, new_split_family)
        self.assertNotEqual(og_timer_family, new_timer_family)

        self.assertEqual(new_title_family, var_map['title-font'])
        self.assertEqual(new_subtitle_family, var_map['subtitle-font'])
        self.assertEqual(new_attempts_family, var_map['attempts-font'])
        self.assertEqual(new_split_family, var_map['split-font'])
        self.assertEqual(new_timer_family, var_map['timer-font'])

    def test_basic_text_setting_update_size(self):
        settings = self.main.settings
        var_map = settings.style.variable_map

        basic_settings = self.main.settings_window.tab_dict['Settings']
        text_settings = basic_settings.text_group

        # setup
        og_title_size = text_settings.title_font_picker.get_size()
        og_subtitle_size = text_settings.subtitle_font_picker.get_size()
        og_attempts_size = text_settings.attempts_font_picker.get_size()
        og_split_size = text_settings.split_font_picker.get_size()
        og_timer_size = text_settings.timer_font_picker.get_size()

        # act
        text_settings.title_font_picker.set_size(og_title_size + 1)
        text_settings.subtitle_font_picker.set_size(og_subtitle_size + 1)
        text_settings.attempts_font_picker.set_size(og_attempts_size + 1)
        text_settings.split_font_picker.set_size(og_split_size + 1)
        text_settings.timer_font_picker.set_size(og_timer_size + 1)

        text_settings.apply()

        # assert
        self.assertNotEqual(text_settings.title_font_picker.get_size(), og_title_size)
        self.assertNotEqual(text_settings.subtitle_font_picker.get_size(), og_subtitle_size)
        self.assertNotEqual(text_settings.attempts_font_picker.get_size(), og_attempts_size)
        self.assertNotEqual(text_settings.split_font_picker.get_size(), og_split_size)
        self.assertNotEqual(text_settings.timer_font_picker.get_size(), og_timer_size)

        self.assertEqual(text_settings.title_font_picker.get_size(), og_title_size + 1)
        self.assertEqual(text_settings.subtitle_font_picker.get_size(), og_subtitle_size + 1)
        self.assertEqual(text_settings.attempts_font_picker.get_size(), og_attempts_size + 1)
        self.assertEqual(text_settings.split_font_picker.get_size(), og_split_size + 1)
        self.assertEqual(text_settings.timer_font_picker.get_size(), og_timer_size + 1)

        self.assertEqual(f'{text_settings.title_font_picker.get_size()}px', var_map['title-size'])
        self.assertEqual(f'{text_settings.subtitle_font_picker.get_size()}px', var_map['subtitle-size'])
        self.assertEqual(f'{text_settings.attempts_font_picker.get_size()}px', var_map['attempts-size'])
        self.assertEqual(f'{text_settings.split_font_picker.get_size()}px', var_map['split-size'])
        self.assertEqual(f'{text_settings.timer_font_picker.get_size()}px', var_map['timer-size'])

    def test_basic_text_setting_update_color(self):
        settings = self.main.settings
        var_map = settings.style.variable_map

        basic_settings = self.main.settings_window.tab_dict['Settings']
        text_settings = basic_settings.text_group

        # setup
        og_title_color = text_settings.title_color_picker.get_color()
        og_subtitle_color = text_settings.subtitle_color_picker.get_color()
        og_session_attempts_color = text_settings.session_attempts_color_picker.get_color()
        og_lifetime_attempts_color = text_settings.lifetime_attempts_color_picker.get_color()
        og_split_color = text_settings.split_color_picker.get_color()
        og_timer_color = text_settings.timer_color_picker.get_color()

        # act
        text_settings.title_color_picker.set_color('#ffffffff')
        text_settings.subtitle_color_picker.set_color('#ffffffff')
        text_settings.session_attempts_color_picker.set_color('#ffffffff')
        text_settings.lifetime_attempts_color_picker.set_color('#ffffffff')
        text_settings.split_color_picker.set_color('#ffffffff')
        text_settings.timer_color_picker.set_color('#ffffffff')

        text_settings.apply()

        # assert
        self.assertNotEqual(text_settings.title_color_picker.get_color(), og_title_color)
        self.assertNotEqual(text_settings.subtitle_color_picker.get_color(), og_subtitle_color)
        self.assertNotEqual(text_settings.session_attempts_color_picker.get_color(), og_session_attempts_color)
        self.assertNotEqual(text_settings.lifetime_attempts_color_picker.get_color(), og_lifetime_attempts_color)
        self.assertNotEqual(text_settings.split_color_picker.get_color(), og_split_color)
        self.assertNotEqual(text_settings.timer_color_picker.get_color(), og_timer_color)

        self.assertEqual(text_settings.title_color_picker.get_color(), QColor('#ffffffff'))
        self.assertEqual(text_settings.subtitle_color_picker.get_color(), QColor('#ffffffff'))
        self.assertEqual(text_settings.session_attempts_color_picker.get_color(), QColor('#ffffffff'))
        self.assertEqual(text_settings.lifetime_attempts_color_picker.get_color(), QColor('#ffffffff'))
        self.assertEqual(text_settings.split_color_picker.get_color(), QColor('#ffffffff'))
        self.assertEqual(text_settings.timer_color_picker.get_color(), QColor('#ffffffff'))

        self.assertEqual(text_settings.title_color_picker.get_color(), QColor(var_map['title-color']))
        self.assertEqual(text_settings.subtitle_color_picker.get_color(), QColor(var_map['subtitle-color']))
        self.assertEqual(text_settings.session_attempts_color_picker.get_color(), QColor(var_map['session-attempts-color']))
        self.assertEqual(text_settings.lifetime_attempts_color_picker.get_color(), QColor(var_map['lifetime-attempts-color']))
        self.assertEqual(text_settings.split_color_picker.get_color(), QColor(var_map['split-color']))
        self.assertEqual(text_settings.timer_color_picker.get_color(), QColor(var_map['timer-color']))
