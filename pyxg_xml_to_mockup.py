import argparse
import os
import sys

import xml.sax

from classes.validator import Validator
from classes.widgetPrinter import WidgetPrinter
from classes.xmlHandler import XMLHandler
from classes.sourceInserter import SourceInserter
from classes.styleInserter import StyleInserter
from classes.sizeInserter import SizeInserter
from classes.guiMaker import GUIMaker

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

parser = xml.sax.make_parser()
parser.setFeature(xml.sax.handler.feature_namespaces, 0)

handler = XMLHandler()
parser.setContentHandler(handler)
parser.parse(xml_path)

sourceInserter = SourceInserter(handler.get_widgets())

styleInserter = StyleInserter(sourceInserter.get_widgets())

WidgetPrinter.print_canvas(styleInserter.get_widgets()[0])

# sizeInserter = SizeInserter(styleInserter.get_canvas(), handler.get_size())

# widgetCreator.print_recursive(sizeInserter.get_canvas())

# guiMaker = GUIMaker(styleInserter.get_widgets(), handler.get_size())
# guiMaker.write_to_file(dest_path)
