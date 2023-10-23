import sys, os, pygame

from ..src.UserInterface import UserInterface

class Program():
    def __init__(self):
        self.win_w, self.win_h = 800, 600
        self.center = (int(self.win_w/2),int(self.win_h/2))
        
        pygame.init()
        self.screen = pygame.display.set_mode((self.win_w, self.win_h))
        self.fpsclock = pygame.time.Clock()
        self.fps = 60

    def main(self):

        with open(os.path.join(os.path.dirname(__file__), "test.xml"), "r") as f:
            structure = f.read()

        points = [
            ("Point A", (1, 5)),
            ("Point B", (4, 9)),
            ("Point C", (15, 20))
        ]
        
        ui = UserInterface()
        ui.set_structure(structure)
        ui.set_variables({
            "points": points
        })
        ui.set_pos((150, 50))
        
        run = True
        while run:
            event_list = pygame.event.get()
            for event in event_list:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
            
            self.screen.fill((0,0,0))
            ui.draw(self.screen)
            ui.update(event_list)
            
            pygame.display.flip()
            self.fpsclock.tick(self.fps)

Program().main()