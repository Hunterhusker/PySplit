import copy


class StyleBuilder:
    def __init__(self):
        self.colors = {}
        self.rawStyleSheet = ""

        self.styleSheet = ""

        self.load_colors()
        self.load_style()

    def load_colors(self):
        with open('colors.qvars', 'r') as f:
            lines = f.readlines()

        for line in lines:
            l_temp = line.replace('\n', '')  # remove the newlines
            k, v = l_temp.split(':')

            self.colors[k] = v

    def set_colors(self):
        pass

    def export_colors(self):
        pass

    def load_style(self):
        with open('style.qss', 'r') as f:
            tmp = f.read()

        self.rawStyleSheet = copy.deepcopy(tmp)

        # replace all the colors
        for k in self.colors.keys():
            tmp.replace(k, self.colors[k])

        self.styleSheet = tmp

    def set_style(self):
        pass

    def export_style(self):
        pass
