import re
import sys

from rich import print as rprint
from classes.widget import Widget
from mmlib import check

REGULAR_EXPRESSION = r"{{.*?}}"

class SourceInserter:
    @check
    def __init__(self, canvas: Widget, variables: dict):
        self.__canvas = canvas
        self.__widgets = canvas.content
        self.__new_widgets = []
        self.__vars = variables
        self.__run()

    def __run(self):
        for widget1 in self.__widgets:
            if widget1.name in ["label", "button"]:
                widget1.content = self.__evaluate_widget(widget1)
                self.__new_widgets.append(widget1)
            if widget1.name == "list":
                l1 = widget1.content
                l2 = []
                for widget2 in l1:
                    if widget2.name in ["label", "button"]:
                        widget2.content = self.__evaluate_widget(widget2)
                        l2.append(widget2)
                    if widget2.name == "list-item":

                        pyForString = widget2.attributes["pyFor"]
                        # 'for v1 in v2'
                        v1 = pyForString.split(" in ")[0]
                        v2 = self.__vars[pyForString.split(" in ")[1]]

                        l3 = widget2.content

                        for item in v2:
                            l5 = []
                            for widget3 in l3:
                                string = self.__evaluate_widget(widget3, {v1: item})
                                l5.append(Widget(widget3.name, widget3.attributes, string))

                            attributes = {k: v for k, v in dict(widget2.attributes).items() if k != "pyFor"}
                            l2.append(Widget("list-item", attributes, l5))

                self.__new_widgets.append(Widget(widget1.name, widget1.attributes, l2))
                print(widget1.attributes)

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
                rprint(f"[red]An error occurred while evaluating the content of a widget (type: {widget.name}, original content: '{widget.content}'):")
                rprint("[red]To be evaluated: ", end="")
                print(match[2:-2])
                rprint("[red]Error: ", end="")
                print(e)
                sys.exit()
            string = string.replace(
                match,
                str(evaluation)
            )

        return string


    def get_canvas(self):
        self.__canvas.content = self.__new_widgets
        return self.__canvas
