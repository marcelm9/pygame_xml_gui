import os
import sys
import time
import pygame

from pygame_xml_gui.src.UserInterface import UserInterface
from pygame_xml_gui.src.classes.errorHandler import ErrorHandler


class UserInterfaceConstructor:
    def __init__(self):
        self.ui = UserInterface()


        self.__structure_path = None
        self.__classes_path = None
        self.__source_path = None
        self.__variabels = None

        # either 'file' or 'vars'
        # exclusive, because that's easier to manage
        self.__source_mode = ""

        self.__space = 20
        self.__refresh_seconds = 1
        self.__background_color = (0, 0, 0)

    def set_structure(self, path: str):
        if not os.path.exists(path):
            ErrorHandler.error(f"Given path {path} does not exist.")
        if not os.path.isfile(path):
            ErrorHandler.error(f"Given path {path} does not point to a file.")
        self.__structure_path = path

    def set_classes(self, path: str):
        if not os.path.exists(path):
            ErrorHandler.error(f"Given path {path} does not exist.")
        if not os.path.isfile(path):
            ErrorHandler.error(f"Given path {path} does not point to a file.")
        self.__classes_path = path

    def set_source(self, path: str):
        if not os.path.exists(path):
            ErrorHandler.error(f"Given path {path} does not exist.")
        if not os.path.isfile(path):
            ErrorHandler.error(f"Given path {path} does not point to a file.")
        self.__source_path = path

    def set_variables(self, variables: dict):
        if not isinstance(variables, dict):
            ErrorHandler.error(f"Given variables object is not of type dict", info=f"found object of type {type(variables)}")
        self.__variabels = variables
    
    def set_space(self, space: int):
        if space < 0:
            ErrorHandler.error(f"Space has to be greater than or equal to zero", info=f"given: {space}")
        self.__space = space

    def set_refresh_interval(self, seconds: float):
        if seconds < 0:
            ErrorHandler.error(f"Interval has to be greater than or equal to 0.5", info=f"given: {seconds}")
        self.__refresh_seconds = seconds

    def set_background_color(self, color: tuple[int, int, int]):
        self.__background_color = color

    def __refresh(self):
        if self.__classes_path is not None:
            self.ui.set_classes(self.__classes_path)

        if self.__source_mode == "file":
            variables = {}
            with open(self.__source_path, "r") as f:
                code = f.read()
            eval(code, None, variables)
            print(f"VARIABLES: {variables}")
            sys.exit(1)
            # TODO: testing
            self.ui.set_variables(variables)
        elif self.__source_mode == "vars":
            self.ui.set_variables(self.__variabels)

        self.ui.set_structure(self.__structure_path)
        
        self.ui.refresh()

        if self.ui.get_rect()[2] != self.__old["width"] or self.ui.get_rect()[3] != self.__old["height"]:
            self.__screen = pygame.display.set_mode((self.ui.get_rect()[2] + self.__space, self.ui.get_rect()[3] + self.__space))
            self.__center = self.__screen.get_rect()[2] // 2, self.__screen.get_rect()[3] // 2
            self.ui.set_pos(self.__center)
            self.__old["width"] = self.__screen.get_rect()[2]
            self.__old["height"] = self.__screen.get_rect()[3]
        

    def run(self):
        if self.__structure_path == None:
            ErrorHandler.error("No structure file given")

        self.__old = {
            "width": -1,
            "height": -1
        }

        pygame.init()
        # TODO: change
        self.__screen = pygame.display.set_mode((100, 100), display=1)
        self.__fpsclock = pygame.time.Clock()
        self.__fps = 60
        self.__center = self.__screen.get_rect()[2] // 2, self.__screen.get_rect()[3] // 2

        self.__last_refresh = time.time() - self.__refresh_seconds - 1
        self.__error = False
        
        run = True
        while run:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
            
            if time.time() - self.__last_refresh > self.__refresh_seconds:
                self.__last_refresh = time.time()
                try:
                    self.__refresh()
                    self.__error = False
                except Exception as e:
                    if self.__error == False:
                        ErrorHandler.error("An error occurred during compilation.", info=e, stop=False)
                    self.__error = True
            
            self.__screen.fill(self.__background_color)
            if self.__error == False:
                self.ui.draw(self.__screen)

            pygame.display.flip()
            self.__fpsclock.tick(self.__fps)

            


