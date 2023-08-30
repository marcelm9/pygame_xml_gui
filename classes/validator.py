#!python3

import sys
import os
import xmlschema

from xml.sax.handler import ContentHandler
from xml.sax import make_parser

from files.paths import TEST_XML_FILE, XSD_FILE
from rich import print as rprint

class Validator:
    def __init__(self, path):
        """This class validates the form of the xml file and its structure.\nCommand: pyxg_validate_xml {path_to_file}"""
        self.path = path
        print("Path: " + str(self.path))

        self.check_form()
        self.check_valid()

    def check_form(self):
        """Checks if the xml file is well-formed"""
        parser = make_parser()
        parser.setContentHandler(ContentHandler())
        rprint("Correct form: ", end="")
        try:
            parser.parse(self.path)
            rprint("[green]Yes[/green]")
        except Exception as e:
            rprint("[red]No[/red]")
            print(f"FormException: {e}")
            sys.exit()

    def check_valid(self):
        """Checks if the xml file is valid against the schema"""
        rprint("Valid: ", end="")
        try:
            xmlschema.validate(self.path, XSD_FILE)
            rprint("[green]Yes[/green]")
        except Exception as e:
            rprint("[red]No[/red]")
            print("StructureException: The following error occurred:")
            print(e)
            sys.exit()
