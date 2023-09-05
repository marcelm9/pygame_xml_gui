from rich import print

from classes.widget import Widget


class GUIMaker:
    def __init__(self, widgets: list[Widget], size: tuple[int, int]):
        self.__widgets = widgets
        self.__gui_widgets = []
        self.__run()

    def __run(self):
        for widget1 in self.__widgets:
            if widget1.name in ["label", "button"]:
                pass

    def write_to_file(self, path):
        pass