import pygame

try:
    import Pygame_Engine as pe
except:
    raise ModuleNotFoundError("It seems like you forgot to install the Pygame_Engine module")

# try:
    # from pygame_xml_gui import SourceInserter, StyleInserter, SizeInserter, GUIMaker
from src.classes.sourceInserter import SourceInserter
from src.classes.styleInserter import StyleInserter
from src.classes.sizeInserter import SizeInserter
from src.classes.guiMaker import GUIMaker
from src.classes.widget import Widget
# except:
    # raise ModuleNotFoundError("It seems like you forgot to install the pygame_xml_gui module")

class Methods:

    def edit(self, entity):
        print("Editing entity with name " + entity.name)

    def round(self, entity):
        print("Rounding entity position of entity with name " + entity.name)

    def delete(self, entity):
        print("Deleting entity with name " + entity.name)

class Canvas:
    def __init__(self, position):
        self.__width, self.__height = 500, 500
        self.__surface = pygame.Surface((self.__width, self.__height))
        self.__position = position
        self.__widget_structure = [
            [Widget(name='canvas', attributes={'pySize': '500x500', 'pySource': 'files/test/data/data.py', 'pyStyle': 'dark', 'pyAxis': 'vertical'},content=[Widget(name='label', attributes={'pyStyle': "padding=0; br=0; bgc=(200,200,200); tc=(20,20,20); to=(10,0); tb='midleft'; f='consolas'; size=16", 'anchor': 'topleft'},content="Entity positions (count: {{len(entities)}})"), Widget(name='list', attributes={'pyMaxHeight': '400', 'pyAxis': 'vertical'},content=[Widget(name='list-item', attributes={'pyFor': 'e in entities', 'pyAxis': 'horizontal'},content=[Widget(name='label', attributes={'pyWidth': '30', 'anchor': 'topleft'},content="{{ e[0].upper() }}"), Widget(name='label', attributes={'pyWidth': '10', 'anchor': 'topleft'},content="{{ e[1] }}"), Widget(name='button', attributes={'pyWidth': '20', 'pyStyle': 'bgc=(30,30,200)', 'pyAction': 'delete', 'pyArgs': 'e', 'anchor': 'topleft'},content="Edit"), Widget(name='button', attributes={'pyWidth': '20', 'anchor': 'topleft'},content="Round"), Widget(name='button', attributes={'pyWidth': '20', 'pyStyle': 'bgc=(200,40,40)', 'anchor': 'topleft'},content="Delete")])])])]
        ]
        self.__widgets = [
            # pe.Button("", "abc", 20, (10,10), tc=(255,255,255), info={"pyAction": "delete", "pyArgs": "e", "context": {"e": Entity("Marcel")}})
        ]
        self.methods = Methods()
        self.__check()

    def __check(self):
        method_list = [func for func in dir(self.methods) if callable(getattr(self.methods, func)) and not func.startswith("__")]

        for widget in self.__widgets:
            if isinstance(widget, pe.Button):
                if widget.info["pyAction"] is not None:
                    if widget.info["pyAction"] not in method_list:
                        raise Exception(f"No function defined for pyAction '{widget.info['pyAction']}'")
                    widget.info["pyArgs"] = self.__evaluate_args(widget)

    def refresh_all_widgets(self, variables):
        widgets = SourceInserter(self.__widget_structure, variables).get_widgets()
        StyleInserter(widgets)
        SizeInserter(widgets)
        self.__widgets = GUIMaker(widgets).get_widgets()

    def set_position(self, position: tuple):
        assert isinstance(position, (tuple, list))
        assert len(position) == 2
        self.__position = tuple(position)
    
    def get_position(self):
        return self.__position

    def update(self, event_list, offset: tuple = (0, 0)):
        for widget in self.__widgets:
            if isinstance(widget, pe.Button):
                if widget.update(event_list, offset) and widget.info["pyAction"] is not None:
                    if widget.info["pyArgs"] != None:
                        self.methods.__getattribute__(widget.info["pyAction"])(*self.__evaluate_args(widget))
                    else:
                        self.methods.__getattribute__(widget.info["pyAction"])()
    
    def TEST_update(self):
        """ pretends that every button in self.__widgets was pressed """
        for widget in self.__widgets:
            if isinstance(widget, pe.Button):
                if widget.info["pyAction"] is not None:
                    if (args := widget.info["pyArgs"]) != None:
                        self.methods.__getattribute__(widget.info["pyAction"])(*args)
                    else:
                        self.methods.__getattribute__(widget.info["pyAction"])()
        print("\n".join([str(w.info) for w in self.__widgets]))

    def draw(self, surface):
        self.__surface.fill((0,0,0))
        for widget in self.__widgets:
            widget.draw_to(self.__surface)
        surface.blit(self.__surface, self.__position)

    def __evaluate_args(self, widget):
        """ args separeted by semicolons """
        locals_ = widget.info["context"] # locals
        args_string = widget.info.get("pyArgs", "")
        args = [arg.strip() for arg in args_string.split(";") if arg.strip() != ""]
        new_args = []
        for arg in args:
            try:
                arg_value = eval(arg, None, locals_)
            except Exception as e:
                raise Exception(f"Error evaluating argument of widget with text '{widget.text}': {e}")
            new_args.append(arg_value)
        del widget.info["context"]
        return new_args
