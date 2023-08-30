from classes.widget import Widget
from rich import print

class WidgetCreator:
    def __init__(self):
        self.__content: list[Widget] = [] # should contain any widgets
        self.__vars = {} # variables from source
    
    def add_widget(self, name, attributes: dict = None, content = None):
        self.__content.append(
            Widget(name, attributes, content)
        )

    def get_widgets(self) -> list[Widget]:
        return self.__content
    
    def set_variables(self, variables):
        self.__vars = variables

    def get_variables(self):
        return self.__vars

    def print_widgets(self, widgets = None):
        if widgets == None:
            widgets_ = self.__content
        else:
            widgets_ = widgets
        for w in widgets_:
            if w.name == "list":
                content: list[Widget] = w.content
                print(f"[purple]name[/purple]: list\nattributes: {dict(w.attributes)}\ncontent:")
                for item in content:
                    if item.name == "list-item":
                        content2: list[Widget] = item.content
                        print(f"|\t[purple]name[/purple]: list-item\n|\tattributes: {dict(item.attributes)}\n|\tcontent:")
                        for item2 in content2:
                            print(f"|\t|\t[purple]name[/purple]: {item2.name}\n|\t|\tattributes: {dict(item2.attributes)}\n|\t|\tcontent: {item2.content}")
                    else:
                        print(f"|\t[purple]name[/purple]: {item.name}\n|\tattributes: {dict(item.attributes)}\n|\tcontent: {item.content}")
            else:
                print(f"[purple]name[/purple]: {w.name}\nattributes: {dict(w.attributes)}\ncontent: {w.content}")
