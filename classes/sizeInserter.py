import sys
from classes.widget import Widget
from mmlib import check

class SizeInserter:
    def __init__(self, canvas: Widget, canvas_size: tuple[int, int]):
        self.__canvas = canvas
        self.__widgets = canvas.content
        self.__new_widgets = []
        self.__size = canvas_size
        self.__standard_width_or_height = 30
        self.__run_recursive(
            self.__canvas, None
        )

    def __run(self):
        canvas = Widget("canvas", {"pyAxis": "vertical", "force_width": self.__size[0]}, None)

        for widget1 in self.__widgets:
            if widget1.name in ["label", "button"]:
                self.__new_widgets.append(self.__get_widget_with_inserted_size(widget1, canvas))
            if widget1.name == "list":
                l1 = widget1.content
                l2 = []
                for widget2 in l1:
                    if widget2.name in ["label", "button"]:
                        l2.append(self.__get_widget_with_inserted_size(widget2, widget1))
                    if widget2.name == "list-item":
                        l3 = widget2.content
                        l4 = []
                        for widget3 in l3:
                            l4.append(self.__get_widget_with_inserted_size(widget3, widget2))
                        l2.append(Widget(widget2.name, widget2.attributes, l4))
                self.__new_widgets.append(Widget(widget1.name, widget2.attributes, l2))

    def __get_widget_with_inserted_size(self, widget: Widget, parent_widget: Widget) -> Widget:
        attributes = dict(widget.attributes)

        if parent_widget.attributes["pyAxis"] == "vertical":
            if "pyWidth" in widget.attributes.keys():
                width = (widget.attributes["pyWidth"] / 100) * parent_widget.attributes["force_width"]
            else:
                width = parent_widget.attributes["force_width"]
            attributes["force_width"] = width
            attributes["force_height"] = self.__standard_width_or_height

        elif parent_widget.attributes["pyAxis"] == "horizontal":
            try:
                height = (widget.attributes["pyHeight"] / 100) * parent_widget.attributes["force_height"]
            except Exception as e:
                print(f"Could not calculate height. Error:")
                print(e)
                height = parent_widget.attributes["force_height"]
            attributes["force_height"] = height
            attributes["force_width"] = self.__standard_width_or_height
        
        return Widget(widget.name, attributes, widget.content)

    def __run_recursive(self, widget: Widget, parent_widget: Widget):
        test_attributes = {
            "abc": 123
        }

        if widget.name == "canvas":
            self.__new_widgets.append(
                Widget(widget.name, widget.attributes, 
                    [
                        self.__run_recursive(item, widget)
                        for item in widget.content
                    ]
                )
            )
        
        if widget.name in ["list", "list-item"]:
            return Widget(widget.name, widget.attributes, 
                    [
                        self.__run_recursive(item, widget)
                        for item in widget.content
                    ]
                )
            

        if widget.name in ["label", "button", "list-item"]:
            for k, v in test_attributes.items():
                widget.attributes[k] = v
            return widget

    def get_canvas(self):
        return self.__canvas
