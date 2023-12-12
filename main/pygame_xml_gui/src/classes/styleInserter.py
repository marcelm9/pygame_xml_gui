import json

from pygame_xml_gui.src.classes.errorHandler import ErrorHandler

from ..files.paths import STYLE_LIGHT, STYLE_DARK
from .widget import Widget

STYLES = {}

with open(STYLE_LIGHT, "r") as f:
    STYLES["light"] = json.load(f)

with open(STYLE_DARK, "r") as f:
    STYLES["dark"] = json.load(f)

class StyleInserter:
    def __init__(self, widgets: list[Widget], classes: dict = None):
        self.__widgets = widgets

        self.__classes: dict = classes

        self.__sanity_check()
        self.__canvas_style: dict = STYLES[self.__widgets[0].attributes["pyStyle"]]

        self.__run()

    def __sanity_check(self):
        assert len(self.__widgets) == 1
        assert self.__widgets[0].name == "canvas"
        assert self.__widgets[0].attributes["pyStyle"] in STYLES.keys()
        if self.__classes is not None:
            assert isinstance(self.__classes, dict)

    def __run(self):
        self.__widgets = [
            self.__run_recursive(widget) for widget in self.__widgets
        ]

    def __run_recursive(self, widget: Widget):
        if widget.name in ["label", "button", "entry"]:
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
        pyStyle_attributes = self.__extract_pyStyle(widget)
        pyClass_attributes = self.__extract_pyClass(widget)

        for k, v in self.__canvas_style.items():
            widget.attributes[k] = v
        
        for k, v in pyClass_attributes.items():
            widget.attributes[k] = v

        for k, v in pyStyle_attributes.items():
            widget.attributes[k] = v

        # this line is necessary for the correct positioning of widgets
        widget.attributes["anchor"] = "topleft"

        return Widget(widget.name, widget.attributes, widget.content)

    def __extract_pyStyle(self, widget: Widget):
        
        if "pyStyle" in widget.attributes.keys():
            styles_dict = {}
            string = widget.attributes["pyStyle"]
            styles = string.split(";")
            styles = [s.strip() for s in styles if s.strip() != ""]
            for style in styles:
                try:
                    key = style.split("=")[0]
                    value = eval(style.split("=")[1])
                    styles_dict[key] = value
                except NameError:
                    raise Exception(f"Could not interpret key-value pair: {style}. Maybe you forgot quotation marks or a semicolon?")
                except:
                    raise Exception(f"Could not interpret key-value pair: {style}")
            return styles_dict
        
        return {}
    
    def __extract_pyClass(self, widget: Widget) -> dict:

        if "pyClass" in widget.attributes.keys() and self.__classes is not None:
            styles_dict = {}
            string = widget.attributes["pyClass"]
            classes = string.split(" ")
            classes = [s.strip() for s in classes if s.strip() != ""]
            for class_ in classes:
                if class_ not in self.__classes.keys():
                    ErrorHandler.error(f"unknown class: {class_}", info=f"known classes: {list(self.__classes.keys())}")
                try:
                    for k, v in self.__classes[class_].items():
                        styles_dict[k] = v
                except Exception:
                    ErrorHandler.error(f"Could not copy attributes of class '{class_}' into widget")
            return styles_dict
        
        return {}
