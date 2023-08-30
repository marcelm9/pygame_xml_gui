import re
import sys
from rich import print as rprint

from classes.widget import Widget

REGULAR_EXPRESSION = r"{{.*?}}"

class SourceInserter:
    def __init__(self, widgets: list[Widget], variables: dict):
        self.__widgets = widgets
        self.__new_widgets = []
        self.__vars = variables
        self.__run()

    def __run(self):
        for widget1 in self.__widgets:
            if widget1.name != "list":
                self.__new_widgets.append(widget1)
            else:
                l1 = widget1.content
                l2 = []
                for widget2 in l1:
                    if widget2.name != "list-item":
                        l2.append(widget2)
                    else:

                        pyForString = widget2.attributes["pyFor"]
                        # 'for v1 in v2'
                        v1 = pyForString.split(" in ")[0]
                        v2 = self.__vars[pyForString.split(" in ")[1]]

                        l3 = widget2.content


                        for item in v2:

                            l5 = []

                            for widget3 in l3:
                                
                                string = widget3.content

                                for match in re.findall(REGULAR_EXPRESSION, string, re.DOTALL):
                                    try:
                                        evaluation = eval(match[2:-2], None, {v1: item})
                                    except Exception as e:
                                        rprint(f"[red]An error occurred while evaluating the content of a widget ({widget3.name} in {widget2.name}):")
                                        rprint("[red]To be evaluated: ", end="")
                                        print(match[2:-2])
                                        rprint("[red]Error: ", end="")
                                        print(e)
                                        sys.exit()
                                    string = string.replace(
                                        match,
                                        str(evaluation)
                                    )

                                l5.append(Widget(widget3.name, widget3.attributes, string))

                            attributes = {k: v for k, v in dict(widget2.attributes).items() if k != "pyFor"}
                            l2.append(Widget("list-item", attributes, l5))

                self.__new_widgets.append(Widget(widget1.name, widget1.attributes, l2))

    def get_widgets(self):
        return self.__new_widgets
