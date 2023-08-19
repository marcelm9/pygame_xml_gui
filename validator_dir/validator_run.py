import argparse
import os

from validator_dir.validator_class import Validator
from validator_dir.cprint import cprint

parser = argparse.ArgumentParser()
parser.add_argument("path", help="Path of the xml file to validate")

args = parser.parse_args()
xml_path = os.path.abspath(args.path)

if not os.path.exists(xml_path):
    cprint(f"Path does not exist: {xml_path}")
if not os.path.isfile(xml_path):
    cprint(f"Path is not a file: {xml_path}")

Validator(xml_path)
