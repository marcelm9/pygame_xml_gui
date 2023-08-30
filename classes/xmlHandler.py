import sys
import os
import xml.sax
from classes.widget import Widget
from classes.widgetCreator import WidgetCreator
from classes.xmlAttributeValidator import XmlAttributeValidator as xav

def error(text):
    print(f"Error: {text}")
    sys.exit()

STYLES = ["light", "dark"]
PRINT = False

class XMLHandler(xml.sax.ContentHandler):
    def __init__(self, widgetCreatorClass: WidgetCreator):
        assert isinstance(widgetCreatorClass, WidgetCreator)
        self.__widgetCreator = widgetCreatorClass


        self.__current_list = []
        self.__current_list_item = []
        self.__current_content = ""

        # for 'list' and 'list-item':
        self.__active = []
        self.__active_attributes = []
        self.__active_contents: list[list] = []

        self.__size = ...
        self.__style = ...
        self.__source = ...

        self.__vars = {}

    def __check_source(self):
        s = os.path.abspath(self.__source)
        if not os.path.exists(s):
            raise Exception(f"Source file does not exist ({s})")
        if not os.path.isfile(s):
            raise Exception(f"Given source file is not a file ({s})")
        if not (str(s).endswith(".py") or str(s).endswith(".pyw")):
            raise Exception(f"Given source file has to be a python file (.py or .pyw)")

    def __import_source(self):
        self.__check_source()
        try:
            with open(self.__source, "r") as f:
                code = f.read()
        except FileNotFoundError:
            print(f"Could not find source file ('{self.__source}')")
        exec(code, None, self.__vars)
        self.__widgetCreator.set_variables(self.__vars)

    def startElement(self, tag, attributes):
        if tag == "canvas":

            size = attributes["pySize"]
            width = int(size.split("x")[0])
            height = int(size.split("x")[1])
            self.__size = (width, height)

            style = attributes["pyStyle"]
            if style not in STYLES: error(f"unknown style ({style})")
            self.__style = style

            if source := attributes["pySource"]:
                self.__source = source
                self.__import_source()
        
        elif tag == "label":
            self.__current_attributes = attributes

        elif tag == "list":
            self.__active.append("list")
            if len(self.__active) > 2:
                error(f"len of self.__active should not be greater than 2 (now: {len(self.__active)})")
            self.__active_attributes.append(attributes)
            self.__active_contents.append([])

        elif tag == "list-item":
            self.__active.append("list-item")
            if len(self.__active) > 2:
                error(f"len of self.__active should not be greater than 2 (now: {len(self.__active)})")
            self.__active_attributes.append(attributes)
            self.__active_contents.append([])

    def characters(self, content: str):
        self.__current_content += content.strip()

    def endElement(self, name):
        if name == "canvas":
            if PRINT:
                print(f"size: {self.__size}\nstyle: {self.__style}\nsource: {self.__source}")
                self.__widgetCreator.print_widgets()
    
        elif name in ["label", "button"]:

            if len(self.__active) > 0:
                if self.__active[-1] == "list":
                    self.__active_contents[-1].append(
                        Widget(name, self.__current_attributes, self.__current_content)
                    )
                elif self.__active[-1] == "list-item":
                    self.__active_contents[-1].append(
                        Widget(name, self.__current_attributes, self.__current_content)
                    )

            else:
                self.__widgetCreator.add_widget(
                    name, self.__current_attributes, self.__current_content
                )

        elif name == "list":
            assert self.__active[-1] == "list", "nothing else should be the case, right?"
            del self.__active[-1]
            assert len(self.__active) == 0, "should be most 'outward' thing right?"
            attributes = self.__active_attributes.pop()
            content = self.__active_contents.pop()
            self.__widgetCreator.add_widget(
                "list", attributes, content
            )

        elif name == "list-item":
            assert self.__active[-1] == "list-item", "nothing else should be the case, right?"
            del self.__active[-1]
            assert len(self.__active) > 0, f"len of self.__active should be greater than 0, because 'list-item' can not be outside 'list'"
            attributes = self.__active_attributes.pop()
            content = self.__active_contents.pop()
            self.__active_contents[-1].append(
                Widget("list-item", attributes, content)
            )
        

        self.__current_content = ""
