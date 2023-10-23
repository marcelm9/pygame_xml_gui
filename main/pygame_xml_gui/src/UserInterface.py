import io
import xml.sax
from xml.sax.xmlreader import InputSource

import Pygame_Engine as pe
import pygame

from rich import print

from .classes.validator import Validator
from .files.schema.xml_schema import SCHEMA
from .classes.xmlHandler import XMLHandler
from .classes.styleInserter import StyleInserter
from .classes.sizeInserter import SizeInserter
from .classes.sourceInserter import SourceInserter
from .classes.guiMaker import GUIMaker


class UserInterface:
    def __init__(self):
        self.__structure_string = None
        self.__structure_widgets = None
        self.__raw_structure_widgets = None
        self.__background = None
        self.__background_color = None
        self.__widgets = None
        self.__variables = None
        self.__methods = None
        self.__pos = (0, 0)
    
    def __process_structure(self):
        if self.__structure_string == None:
            raise Exception("no structure given")
        if not isinstance(self.__structure_string, str):
            raise Exception("given structure is not a string")
        
        # validate structure
        Validator(self.__structure_string, SCHEMA)

        # transform structure from xml to widgets
        parser = xml.sax.make_parser()
        parser.setFeature(xml.sax.handler.feature_namespaces, 0)
        handler = XMLHandler()
        parser.setContentHandler(handler)
        inpsrc = InputSource()
        inpsrc.setCharacterStream(io.StringIO(self.__structure_string))
        parser.parse(inpsrc)

        # get structure
        widgets = handler.get_widget_structure()

        # inject style
        StyleInserter(widgets)

        # inject size
        SizeInserter(widgets)

        self.__raw_structure_widgets = widgets.copy()

    def set_structure(self, structure: str):
        """
        Set the structure of the UI.
        
        'structure' should be a string of an xml file that adheres to
        the rules specified in the pygame_xml_gui schema. The schema
        can be found at pygame_xml_gui/src/files/schema/xml_schema.xsd.
        """
        self.__structure_string = structure
        self.__process_structure()
    
    def update(self, event_list, button: int = 1, offset: tuple = (0, 0)):
        real_offset = (offset[0] + self.__pos[0], offset[1] + self.__pos[1])
        for widget in self.__widgets:
            if isinstance(widget, pe.Button):
                if widget.update(event_list, button, real_offset):
                    print("a button has been pressed")

    def set_variables(self, variables: dict):
        self.__variables = variables
        self.refresh()

    def refresh(self):
        # TODO: callable only if structure is set (and variables are not None?)
        # for now:
        assert self.__raw_structure_widgets != None
        assert self.__variables != None

        # does this also change self.__raw_structure_widgets ?
        self.__structure_widgets = SourceInserter(self.__raw_structure_widgets, self.__variables).get_widgets()
        gm = GUIMaker(self.__structure_widgets)
        self.__widgets: list[pe.Label | pe.Button] = gm.get_widgets()
        self.__background = pygame.Surface(gm.get_size())
        self.__background_color = gm.get_background_color()
    
    def set_pos(self, position_topleft: tuple[int, int]):
        self.__pos = position_topleft

    def draw(self, screen: pygame.Surface):
        #! FOR NOW JUST GREEN; IDK WHY
        self.__background.fill(self.__background_color)
        for widget in self.__widgets:
            widget.draw_to(self.__background)
        screen.blit(self.__background, self.__pos)

        
    








