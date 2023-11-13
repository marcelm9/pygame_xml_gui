import sys, os, pygame

from ..src.UserInterface import UserInterface
import random

from Pygame_Engine import PerformanceGraph

RUN_FOR = -1 # seconds

class Shift:
    def __init__(self, type_, car, crew, start, end):
        self.type = type_
        self.car = car
        self.crew = crew
        self.start = start
        self.end = end

class Program():
    def __init__(self):
        self.win_w, self.win_h = 800, 600
        self.center = (int(self.win_w/2),int(self.win_h/2))
        
        pygame.init()
        self.screen = pygame.display.set_mode((self.win_w, self.win_h))
        self.fpsclock = pygame.time.Clock()
        self.fps = 60

    def main(self):

        fpslist = []

        with open(os.path.join(os.path.dirname(__file__), "test_dp.xml"), "r") as f:
            structure = f.read()

        shift = Shift("JOK", "A-39", ["Marcel Menzel", "Lena Hofmann"], "15.11.2023, 10:00", "15.11.2023, 18:30")
        
        self.ui = UserInterface()
        self.ui.set_structure(structure)
        self.ui.set_variables({
            "type_": shift.type,
            "car": shift.car,
            "crew": shift.crew,
            "start": shift.start,
            "end": shift.end
        })
        self.ui.set_pos((150, 50))
        
        run = True
        while run:
            event_list = pygame.event.get()
            for event in event_list:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run = False
            
            self.screen.fill((0,0,0))
            # ui.refresh()
            self.ui.draw(self.screen)
            fps = self.fpsclock.get_fps()
            fpslist.append(fps)
            pygame.display.set_caption("Seconds left: " + str(round(RUN_FOR - (len(fpslist)/self.fps), 2)))
            if len(fpslist) == RUN_FOR * self.fps:
                run = False
            
            
            pygame.display.flip()
            self.fpsclock.tick(self.fps)

        pygame.display.set_caption("PerformanceGraph")
        PerformanceGraph(60, fpslist)
        
        

Program().main()