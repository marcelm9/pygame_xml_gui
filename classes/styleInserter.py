import json

from mmlib import check
from files.paths import STYLE_LIGHT, STYLE_DARK
from classes.widget import Widget

STYLES = {}

with open(STYLE_LIGHT, "r") as f:
    STYLES["light"] = json.load(f)

with open(STYLE_DARK, "r") as f:
    STYLES["dark"] = json.load(f)

class StyleInserter:
    @check
    def __init__(self, widgets: list[Widget]):
        self.__widgets = widgets
        self.__new_widgets = []

        self.__sanity_check()
        self.__style: dict = STYLES[self.__widgets[0].attributes["pyStyle"]]

        self.__run()

    def __sanity_check(self):
        assert len(self.__widgets) == 1
        assert self.__widgets[0].name == "canvas"
        assert self.__widgets[0].attributes["pyStyle"] in STYLES.keys()

    def __run(self):
        self.__new_widgets = [
            self.__run_recursive(widget) for widget in self.__widgets
        ]

    def __run_recursive(self, widget: Widget):
        if widget.name in ["label", "button"]:
            return self.__get_widget_with_injected_style_attributes(widget)
        elif widget.name in ["canvas", "list", "list-item"]:
            return Widget(
                widget.name,
                widget.attributes,
                [
                    self.__run_recursive(item) for item in widget.content
                ]
            )

    def __get_widget_with_injected_style_attributes(self, widget: Widget) -> Widget:
        attributes = widget.attributes
        for k, v in self.__style.items():
            if k not in attributes.keys():
                attributes[k] = v
        return Widget(widget.name, attributes, widget.content)
    
    def get_widgets(self):
        return self.__new_widgets