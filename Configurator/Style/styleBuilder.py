import copy
import json

from PySide6.QtCore import Signal


class StyleBuilder:
    UpdateStyle = Signal(str)

    def __init__(self, style_path, vars_path):
        self.style_path = style_path
        self.vars_path = vars_path

        self.variable_map = {}
        self.raw_style_sheet = ""

        self.formatted_style_sheet = ""

        self.load_vars()
        self.load_style()

    def load_vars(self):
        with open(self.vars_path, 'r') as f:
            lines = f.readlines()

        for line in lines:
            l_temp = line.replace('\n', '')  # remove the newlines
            k, v = l_temp.split(':')

            self.variable_map[k] = v

    def set_vars(self, variable_map):
        self.variable_map = variable_map

    def export_vars(self):
        """
        Build the variable map and save it to the file
        """
        tmp = ''

        for k, v in self.variable_map.items():
            tmp += f'{k}:{v}'

        with open(self.vars_path, 'w') as f:
            f.write(tmp)

    def load_style(self):
        with open(self.style_path, 'r') as f:
            tmp = f.read()

        self.raw_style_sheet = tmp

        self.format_style()

    def set_style(self, styleSheet):
        self.formatted_style_sheet = styleSheet

    def format_style(self):
        tmp = copy.deepcopy(self.raw_style_sheet)

        # replace all the colors
        for k, v in self.variable_map.items():
            tmp = tmp.replace('$' + k, v)

        self.formatted_style_sheet = tmp

    def export_style(self):
        with open(self.style_path, 'w') as f:
            f.write(self.raw_style_sheet)

    def update_style(self, style_sheet: str = None, var_map: dict[str: str] = None):
        """
        Takes in new stylesheet data, or nothing, applies it to itself, and then emits a signal to refresh the style

        Args:
            style_sheet: (str, optional) the raw style sheet that we want to update the style to
            var_map: (dict[str: str], optional) the mapping of the variables that we want to update our SASS with

        Emits:
            UpdateStyle: A signal that you can subscribe to know when the style sheet changes
        """
        if style_sheet is not None:
            self.set_style(style_sheet)

        if var_map is not None:
            self.set_vars(var_map)

        print()

        self.format_style()  # format the sheet with the updated data

        #self.UpdateStyle.emit(self.formatted_style_sheet)  # emit the changed sheet

    def update_style_from_paths(self, style_path: str = None, vars_path: str = None):
        """
        Calls the update method but by first reading the data from the files

        Args:
            style_path: (str) the path to the file containing the style info
            vars_path: (str) the path to the file containing the variable declarations

        Returns:
            None
        """
        if style_path is not None:
            self.style_path = style_path

            with open(style_path, 'r') as f:
                self.raw_style_sheet = f.read()

        if vars_path is not None:
            self.vars_path = vars_path
            self.load_vars()

        self.update_style(self.raw_style_sheet, self.variable_map)
