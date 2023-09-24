import argparse
import os
import sys

from classes.validator import Validator

parser = argparse.ArgumentParser()
parser.add_argument("path", help="Path of the xml file to validate")

args = parser.parse_args()
xml_path = os.path.abspath(args.path)

if not os.path.exists(xml_path):
    print(f"Path does not exist: {xml_path}")
    sys.exit()
if not os.path.isfile(xml_path):
    print(f"Path is not a file: {xml_path}")
    sys.exit()

Validator(xml_path)
