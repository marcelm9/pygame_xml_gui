import sys
from classes.widget import Widget
from mmlib import check

class SizeInserter:
    def __init__(self, widgets: list[Widget]):
        self.__widgets = widgets
        self.__new_widgets = []
        self.__sanity_check()

        self.__standard_width_or_height = 30
        self.__run()

    def __sanity_check(self):
        assert len(self.__widgets) == 1
        assert self.__widgets[0].name == "canvas"

    def __run(self):
        self.__new_widgets = [
            self.__run_recursive(widget, None) for widget in self.__widgets
        ]

    def __run_recursive(self, widget: Widget, parent_widget_attributes: dict):

        if widget.name == "canvas":
            widget_attributes = widget.attributes
            width = int(widget.attributes["pySize"].split("x")[0])
            widget_attributes["force_width"] = width
            # only setting "force_width" for now
            return Widget(
                widget.name,
                widget_attributes,
                [
                    self.__run_recursive(item, widget_attributes) for item in widget.content
                ]
            )

        if widget.name in ["list", "list-item"]:
            widget_attributes = widget.attributes
            width = parent_widget_attributes["force_width"]
            widget_attributes["force_width"] = width
            return Widget(widget.name, widget.attributes, 
                    [
                        self.__run_recursive(item, widget_attributes) for item in widget.content
                    ]
                )


        if widget.name in ["label", "button"]:
            return self.__get_widget_with_inserted_size(widget, parent_widget_attributes)

    def __get_widget_with_inserted_size(self, widget: Widget, parent_widget_attributes: dict) -> Widget:
        attributes = widget.attributes

        if "pyWidth" in widget.attributes.keys():
            width = (int(widget.attributes["pyWidth"]) / 100) * parent_widget_attributes["force_width"]
            del attributes["pyWidth"]
        else:
            width = parent_widget_attributes["force_width"]
        attributes["force_width"] = width
        attributes["force_height"] = self.__standard_width_or_height
        
        return Widget(widget.name, attributes, widget.content)

    def get_widgets(self):
        return self.__widgets
