from rich import print

from classes.widget import Widget
from Pygame_Engine import Label, Button
import pygame
pygame.init()


class GUIMaker:
    def __init__(self, widgets: list[Widget]):
        self.__widgets = widgets
        self.__gui_widgets = []
        self.__text_gui_widgets = []
        self.__sanity_check()
        self.__run()

    def __sanity_check(self):
        assert len(self.__widgets) == 1
        assert self.__widgets[0].name == "canvas"

    def __run(self):
        self.__current_x = 0
        self.__current_y = 0
        self.__run_recursive(self.__widgets[0], None)

    def __run_recursive(self, widget: Widget, parent_attributes: dict):

        if widget.name in ["label", "button"]:
            w = Label if widget.name == "label" else Button
            size = widget.attributes["size"]
            anchor = widget.attributes["anchor"]
            attributes = {k: v for k, v in widget.attributes.items() if k not in ["pyWidth", "size", "anchor"]}
            self.__gui_widgets.append(
                w(None, widget.content, size, self.__pos(), anchor, **attributes)
            )

            attributes_text = f'None, "{widget.content}", {size}, {self.__pos()}, "{anchor}"'
            for k, v in attributes.items():
                value = "\"" + v + "\"" if isinstance(v, str) else v
                attributes_text += f", {k}={value}"
            self.__text_gui_widgets.append(
                widget.name.title() + f"({attributes_text})"
            )

            if parent_attributes["pyAxis"] == "vertical":
                self.__current_y += self.__gui_widgets[-1].rect.height
            elif parent_attributes["pyAxis"] == "horizontal":
                self.__current_x += self.__gui_widgets[-1].rect.width

        elif widget.name in ["canvas", "list"]:
            for item in widget.content:
                self.__run_recursive(item, widget.attributes)
        
        elif widget.name == "list-item":
            x, y = self.__pos()
            for item in widget.content:
                self.__run_recursive(item, widget.attributes)
            self.__set_pos(x, y + self.__gui_widgets[-1].rect.height)


    def __pos(self):
        return self.__current_x, self.__current_y
    
    def __set_pos(self, x = None, y = None):
        if x is not None:
            self.__current_x = x
        if y is not None:
            self.__current_y = y

    def write_to_file(self, path):
        size = self.__widgets[0].attributes["pySize"].split("x")
        size = int(size[0]), int(size[1])
        code = []
        code.append("import pygame")
        code.append("import sys")
        code.append("import Pygame_Engine as pe")
        code.append("")
        code.append("pygame.init()")
        code.append(f"screen = pygame.display.set_mode({size})")
        code.append("fpsclock = pygame.time.Clock()")
        code.append("fps = 60")
        code.append("")
        code.append("widgets = [")
        for item in self.__text_gui_widgets:
            code.append(f"\tpe.{item},")
        code.append("]")
        code.append("")
        code.append("while True:")
        code.append("\tevents = pygame.event.get()")
        code.append("\tfor e in events:")
        code.append("\t\tif e.type == pygame.QUIT:")
        code.append("\t\t\tpygame.quit()")
        code.append("\t\t\tsys.exit()")
        code.append("\tfor widget in widgets:")
        code.append("\t\tif isinstance(widget, pe.Button):")
        code.append("\t\t\twidget.update(events)")
        code.append("\tscreen.fill((80,80,200))")
        code.append("\tfor item in widgets:")
        code.append("\t\titem.draw_to(screen)")
        code.append("\tpygame.display.flip()")
        code.append("\tfpsclock.tick(fps)")
        code.append("")

        with open(path, "w") as f:
            f.write("\n".join(code))
            print(f"[green]Written code to file {path}")
