import re
import sys
import os

from rich import print as rprint
from pprint import pprint as print
from classes.widget import Widget
from mmlib import check

REGULAR_EXPRESSION = r"{{.*?}}"


class SourceInserter:
    @check
    def __init__(self, widgets: list[Widget]):
        self.__widgets = widgets
        self.__new_widgets = []

        self.__sanity_check()
        self.__source = self.__widgets[0].attributes.get("pySource", None)
        self.__vars = {}
        self.__import_source()
        self.__run()

    def __sanity_check(self):
        assert len(self.__widgets) == 1
        assert self.__widgets[0].name == "canvas"

    def __import_source(self):
        if self.__source == None:
            return

        # checking for errors
        s = os.path.abspath(self.__source)
        if not os.path.exists(s):
            raise Exception(f"Source file does not exist ({s})")
        if not os.path.isfile(s):
            raise Exception(f"Given source file is not a file ({s})")
        if not (str(s).endswith(".py") or str(s).endswith(".pyw")):
            raise Exception(f"Given source file has to be a python file (.py or .pyw)")

        # trying to load the variables
        try:
            with open(self.__source, "r") as f:
                code = f.read()
        except FileNotFoundError:
            print(f"Could not find source file ('{self.__source}')")
        exec(code, None, self.__vars)

    def __run(self):
        self.__new_widgets = [
            self.__run_recursive(widget, None, {}) for widget in self.__widgets
        ]
        self.__unpack_lists()

    def __run_recursive(
        self, widget: Widget, parent_widget: Widget | None, additional_variables: dict
    ):
        if widget.name in ["canvas", "list"]:
            return Widget(
                widget.name,
                widget.attributes,
                [self.__run_recursive(item, widget, additional_variables) for item in widget.content],
            )
        elif widget.name in ["label", "button"]:
            return self.__evaluate_widget(
                widget, additional_variables
            )  # TODO: insert source
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
                        self.__run_recursive(
                            widget_in_list_item,
                            widget,
                            {v1: variable_value}
                            ),
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

    @check
    def __evaluate_widget(self, widget: Widget, additional_locals: dict | None = None):
        assert widget.name in ["label", "button"]
        string = widget.content

        vars_ = self.__vars.copy()

        if additional_locals != None:
            for k, v in additional_locals.items():
                vars_[k] = v

        for match in re.findall(REGULAR_EXPRESSION, string, re.DOTALL):
            try:
                evaluation = eval(match[2:-2], None, vars_)
            except Exception as e:
                rprint(
                    f"[red]An error occurred while evaluating the content of a widget (type: {widget.name}, original content: '{widget.content}'):"
                )
                rprint("[red]To be evaluated: ", end="")
                print(match[2:-2])
                rprint("[red]Error: ", end="")
                print(e)
                sys.exit()
            string = string.replace(match, str(evaluation))

        return Widget(widget.name, widget.attributes, string)

    def get_widgets(self):
        return self.__new_widgets
