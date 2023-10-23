import argparse
import os

import xml.sax

from classes.validator import Validator
from classes.xmlHandler import XMLHandler
from classes.classWriter import ClassWriter
from classes.check import Check

parser = argparse.ArgumentParser()
parser.add_argument("path", help="Path of the xml file to create a mockup from")
parser.add_argument("dest", help="Path of the class file")

args = parser.parse_args()
xml_path = os.path.abspath(args.path)
dest_path = os.path.abspath(args.dest)

Check.xml_path(xml_path)
Check.output_path(dest_path)

print(f"XML path: {xml_path}")
print(f"Output path: {dest_path}")

Validator(xml_path)

parser = xml.sax.make_parser()
parser.setFeature(xml.sax.handler.feature_namespaces, 0)

handler = XMLHandler()
parser.setContentHandler(handler)
parser.parse(xml_path)

# a recursive list containing Widget classes
widget_structure = handler.get_widgets()

ClassWriter(
    widget_structure=widget_structure
).to_file(dest_path)
