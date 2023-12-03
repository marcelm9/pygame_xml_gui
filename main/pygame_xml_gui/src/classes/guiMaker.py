import sys
from rich import print

from .widget import Widget
from PygameXtras import Label, Button
import pygame
pygame.init()


class GUIMaker:
    def __init__(self, widgets: list[Widget]):
        self.__widgets = widgets
        self.__gui_widgets = []

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
            size = widget.attributes["size"]
            anchor = widget.attributes["anchor"]
            attributes = {k: v for k, v in widget.attributes.items() if (k not in ["size", "anchor", "contextInfo", "info"] and not k.startswith("py"))}
            attributes["info"] = {}

            if widget.name == "label":
                self.__gui_widgets.append(
                    Label(None, widget.content, size, self.__pos(), anchor, **attributes)
                )
            elif widget.name == "button":
                attributes["info"] = {
                    "pyAction": widget.attributes.get("pyAction", None),
                    "pyArgs": widget.attributes.get("pyArgs", None)
                }
                self.__gui_widgets.append(
                    Button(None, widget.content, size, self.__pos(), anchor, **attributes)
                )

            # testing the widget
            # fails for invalid inputs that are not caught by the __init__ method of Label / Button
            try:
                self.__gui_widgets[-1].draw_to(pygame.Surface((10,10)))
            except:
                print("[red]Could not create GUI widget due to invalid attribute(s):")
                print(attributes)
                sys.exit()

            # positioning
            if parent_attributes["pyAxis"] == "vertical":
                # move down
                self.__current_y += self.__gui_widgets[-1].rect.height
            elif parent_attributes["pyAxis"] == "horizontal":
                self.__current_x += self.__gui_widgets[-1].rect.width
            # print(f"{self.__layout_remainder = } ( - 1)")
            # self.__layout_remainder -= 1
            # if parent_attributes["pyAxis"] == "vertical":
            #     # move down
            #     if self.__layout_remainder > 0:
            #         self.__current_x += self.__gui_widgets[-1].rect.width
            #     else:
            #         if self.__custom_layout_remaining():
            #             self.__layout_remainder = self.__custom_layout[0]
            #             del self.__custom_layout[0]
            #         else:
            #             self.__layout_remainder = self.__default_layout
            #         self.__set_pos(0, self.__current_y + self.__gui_widgets[-1].rect.height)
            # elif parent_attributes["pyAxis"] == "horizontal":
            #     # move right
            #     self.__current_x += self.__gui_widgets[-1].rect.width

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
        with open(path, "w") as f:
            f.write(self.__write_code())
            print(f"[green]Written code to file {path}")

    def get_widgets(self):
        return self.__gui_widgets
    
    def get_background_color(self) -> tuple[int, int, int]:
        return eval(self.__widgets[0].attributes["pyBackground"])
    
    def get_size(self):
        return [int(number) for number in self.__widgets[0].attributes["pySize"].split("x")]
