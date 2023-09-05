import json

from mmlib import check
from files.paths import STYLE_LIGHT, STYLE_DARK
from classes.widget import Widget

styles = {}

with open(STYLE_LIGHT, "r") as f:
    styles["light"] = json.load(f)

with open(STYLE_DARK, "r") as f:
    styles["dark"] = json.load(f)

class StyleInserter:
    @check
    def __init__(self, canvas: Widget, style: str):
        assert style in ["light", "dark"]
        self.__canvas = canvas
        self.__widgets = canvas.content
        self.__new_widgets = []
        self.__style = styles[style]
        self.__run()

    def __run(self):
        for widget1 in self.__widgets:
            if widget1.name in ["label", "button"]:
                self.__new_widgets.append(self.__get_widget_with_injected_style_attributes(widget1))
            if widget1.name == "list":
                l1 = widget1.content
                l2 = []
                for widget2 in l1:
                    if widget2.name in ["label", "button"]:
                        l2.append(self.__get_widget_with_injected_style_attributes(widget2))
                    if widget2.name == "list-item":
                        l3 = widget2.content
                        l4 = []
                        for widget3 in l3:
                            l4.append(self.__get_widget_with_injected_style_attributes(widget3))
                        l2.append(Widget(widget2.name, widget2.attributes, l4))
                self.__new_widgets.append(Widget(widget1.name, widget2.attributes, l2))


    def __get_widget_with_injected_style_attributes(self, widget: Widget) -> Widget:
        attributes = dict(widget.attributes)
        for k, v in self.__style.items():
            if k not in attributes.keys():
                attributes[k] = v
        return Widget(widget.name, attributes, widget.content)
    
    def get_canvas(self):
        self.__canvas.content = self.__new_widgets
        return self.__canvas

