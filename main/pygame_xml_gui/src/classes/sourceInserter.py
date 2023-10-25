import re

from rich import print
from .widget import Widget

REGULAR_EXPRESSION = r"{{.*?}}"


class SourceInserter:
    def __init__(self, widgets: list[Widget], variables):
        self.__widgets = widgets
        self.__new_widgets = []

        self.__sanity_check()
        self.__vars = variables
        self.__run()

    def __sanity_check(self):
        assert len(self.__widgets) == 1
        assert self.__widgets[0].name == "canvas"

    def __run(self):
        self.__new_widgets = [
            self.__run_recursive(widget, {}) for widget in self.__widgets
        ]
        self.__unpack_lists()

    def __run_recursive(self, widget: Widget, additional_variables: dict):
        if widget.name in ["canvas", "list"]:
            return Widget(
                widget.name,
                widget.attributes,
                [
                    self.__run_recursive(item, additional_variables)
                    for item in widget.content
                ],
            )
        elif widget.name in ["label", "button"]:
            return self.__evaluate_widget(
                widget, additional_variables
            )
        elif widget.name == "list-item":
            return_list = []
            v1 = widget.attributes["pyFor"].split(" in ")[0]  # name of the iterable
            v2 = self.__vars[
                widget.attributes["pyFor"].split(" in ")[1]
            ]  # list of items to iterate over

            for variable_value in v2:
                content = []
                for widget_in_list_item in widget.content:
                    content.append(
                        self.__run_recursive(widget_in_list_item, {v1: variable_value}),
                    )
                return_list.append(content)
            return [
                Widget(
                    widget.name,
                    {  # removes pyFor attribute
                        k: v for k, v in dict(widget.attributes).items() if k != "pyFor"
                    },
                    collection,
                )
                for collection in return_list
            ]

    def __unpack_lists(self):
        self.__unpacked_widgets = [
            self.__unpack_recursive(widget) for widget in self.__new_widgets
        ]
        self.__new_widgets = self.__unpacked_widgets

    def __unpack_recursive(self, widget: Widget):
        if widget.name in ["label", "button"]:
            return widget

        if widget.name in ["list"]:
            new_content = []
            for item in widget.content:
                if isinstance(item, list):
                    for inner_item in item:
                        new_content.append(self.__unpack_recursive(inner_item))
                else:
                    new_content.append(self.__unpack_recursive(item))
            return Widget(widget.name, widget.attributes, new_content)

        if widget.name in ["canvas", "list-item"]:
            return Widget(
                widget.name,
                widget.attributes,
                [self.__unpack_recursive(item) for item in widget.content],
            )

    def __evaluate_widget(self, widget: Widget, additional_locals: dict | None = None):
        assert widget.name in ["label", "button"]
        new_widget_attributes = widget.attributes.copy()
        string = widget.content

        vars_ = self.__vars.copy()

        if additional_locals != None:
            for k, v in additional_locals.items():
                vars_[k] = v

        for match in re.findall(REGULAR_EXPRESSION, string, re.DOTALL):
            to_be_evaluated = match[2:-2]
            evaluation = ""
            if to_be_evaluated.strip() != "":
                try:
                    evaluation = eval(to_be_evaluated, None, vars_)
                except Exception:
                    raise Exception(
                        f"An error occurred while evaluating the content of a widget (type: {widget.name}, original content: '{widget.content}')"
                        + f"\nContent to be evaluated: '{to_be_evaluated}'"
                    )
            string = string.replace(match, str(evaluation))

        # adding the context (the local variables of the pyFor) to the attributes
        new_widget_attributes["contextInfo"] = additional_locals

        # evaluating pyArgs for button
        if widget.name == "button":
            raw_pyArgs = widget.attributes["pyArgs"]
            try:
                pyArgs = eval(raw_pyArgs, None, vars_)
            except Exception:
                raise Exception(
                    f"An error occurred while evaluating attribute 'pyArgs' for a widget (type: {widget.name}, content: '{widget.content}')"
                    + f"\nContent to be evaluated: '{raw_pyArgs}'"
                )
            new_widget_attributes["pyArgs"] = pyArgs


        return Widget(widget.name, new_widget_attributes, string)

    def get_widgets(self):
        return self.__new_widgets
