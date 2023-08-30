import argparse
import os
import sys

import xml.sax

from classes.validator import Validator
from classes.widgetCreator import WidgetCreator
from classes.xmlHandler import XMLHandler
from classes.sourceInserter import SourceInserter

parser = argparse.ArgumentParser()
parser.add_argument("path", help="Path of the xml file to create a mockup from")
parser.add_argument("dest", help="Path of the mockup file")

args = parser.parse_args()
xml_path = os.path.abspath(args.path)
dest_path = os.path.abspath(args.dest)

if not os.path.exists(xml_path):
    print(f"Path does not exist: {xml_path}")
    sys.exit()
if not os.path.isfile(xml_path):
    print(f"Path is not a file: {xml_path}")
    sys.exit()

if not (dest_path.endswith(".py") or dest_path.endswith(".pyw")):
    print(f"Destination path has to be a python file (.py or .pyw)")
    sys.exit()

Validator(xml_path)

widgetCreator = WidgetCreator()

parser = xml.sax.make_parser()
parser.setFeature(xml.sax.handler.feature_namespaces, 0)

handler = XMLHandler(widgetCreator)
parser.setContentHandler(handler)
parser.parse(xml_path) # inserts widgets into WidgetCreator
# widgetCreator.print_widgets()

sourceInserter = SourceInserter(widgetCreator.get_widgets(), widgetCreator.get_variables())
widgets = widgetCreator.print_widgets(sourceInserter.get_widgets())

