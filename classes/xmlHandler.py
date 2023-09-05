import sys
import os
import xml.sax
from classes.widget import Widget

def error(text):
    print(f"Error: {text}")
    sys.exit()

STYLES = ["light", "dark"]
PRINT = False

class XMLHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.__widgets = []

        # for any widget that stores other widgets
        self.__active_names = []
        self.__active_attributes = []
        self.__active_contents = []

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
        if tag in ["canvas", "list", "list-item"]:
            self.__active_names.append(tag)
            self.__active_attributes.append(attributes)
            self.__active_contents.append([])
        elif tag in ["label", "button"]:
            self.__active_names.append(tag)
            self.__active_attributes.append(attributes)
            self.__active_contents.append("")

    def characters(self, content: str):
        if content.strip() == "":
            return
        self.__active_contents[-1] = self.__active_contents[-1] + content.strip()

    def endElement(self, name):
        w_name = self.__active_names.pop()
        w_attributes = dict(self.__active_attributes.pop())
        w_content = self.__active_contents.pop()
        widget = Widget(w_name, w_attributes, w_content)
        if name == "canvas":
            self.__widgets.append(widget)
        else:
            self.__active_contents[-1].append(widget)

    def get_widgets(self):
        return self.__widgets
