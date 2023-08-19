#!python3

import sys
import os
import xmlschema

from xml.sax.handler import ContentHandler
from xml.sax import make_parser

from validator_dir.cprint import cprint

class Validator:
    def __init__(self, path):
        """This class validates the form of the xml file and its structure.\nCommand: pyxg_validate_xml {path_to_file}"""
        self.path = path
        cprint("Path: " + str(self.path))

        self.check_form()
        self.check_valid()

    def check_form(self):
        """Checks if the xml file is well-formed"""
        parser = make_parser()
        parser.setContentHandler(ContentHandler())
        try:
            parser.parse(self.path)
            cprint("Good form")
        except Exception as e:
            cprint(f"FormException: {e}")
            sys.exit()

    def check_valid(self):
        """Checks if the xml file is valid against the schema"""
        xsd = os.path.join("validator_dir", "xml_schema.xsd")
        try:
            xmlschema.validate(self.path, xsd)
            cprint("XML valid")
        except Exception as e:
            cprint("StructureException: The following error occurred:")
            print(e)
            sys.exit()
