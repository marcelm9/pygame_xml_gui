import pygame
import sys
import Pygame_Engine as pe

pygame.init()
screen = pygame.display.set_mode((500, 500))
fpsclock = pygame.time.Clock()
fps = 60

widgets = [
	pe.Label(None, "Entity positions (count: 2)", 22, (0, 0), "topleft", tc=[250, 250, 250], bgc=[40, 40, 40], hl=1, br=4, force_width=500, force_height=30),
	pe.Label(None, "Pascal", 22, (0, 31), "topleft", tc=[250, 250, 250], bgc=[40, 40, 40], hl=1, br=4, force_width=150, force_height=30),
	pe.Label(None, "(1, 1)", 22, (151, 31), "topleft", tc=[250, 250, 250], bgc=[40, 40, 40], hl=1, br=4, force_width=50, force_height=30),
	pe.Button(None, "Change", 22, (202, 31), "topleft", tc=[250, 250, 250], bgc=[40, 40, 40], hl=1, br=4, force_width=100, force_height=30),
	pe.Button(None, "Round", 22, (303, 31), "topleft", tc=[250, 250, 250], bgc=[40, 40, 40], hl=1, br=4, force_width=100, force_height=30),
	pe.Button(None, "Delete", 22, (404, 31), "topleft", tc=[250, 250, 250], bgc=[40, 40, 40], hl=1, br=4, force_width=100, force_height=30),
	pe.Label(None, "Marcel", 22, (0, 62), "topleft", tc=[250, 250, 250], bgc=[40, 40, 40], hl=1, br=4, force_width=150, force_height=30),
	pe.Label(None, "(2, 2)", 22, (151, 62), "topleft", tc=[250, 250, 250], bgc=[40, 40, 40], hl=1, br=4, force_width=50, force_height=30),
	pe.Button(None, "Change", 22, (202, 62), "topleft", tc=[250, 250, 250], bgc=[40, 40, 40], hl=1, br=4, force_width=100, force_height=30),
	pe.Button(None, "Round", 22, (303, 62), "topleft", tc=[250, 250, 250], bgc=[40, 40, 40], hl=1, br=4, force_width=100, force_height=30),
	pe.Button(None, "Delete", 22, (404, 62), "topleft", tc=[250, 250, 250], bgc=[40, 40, 40], hl=1, br=4, force_width=100, force_height=30),
	pe.Label(None, "no formatting here, right? (a = 1)", 22, (0, 93), "topleft", tc=[250, 250, 250], bgc=[40, 40, 40], hl=1, br=4, force_width=500, force_height=30),
	pe.Label(None, "All entities started from position (0, 0)", 22, (0, 124), "topleft", tc=[250, 250, 250], bgc=[40, 40, 40], hl=1, br=4, force_width=500, force_height=30),
]

while True:
	events = pygame.event.get()
	for e in events:
		if e.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
	for widget in widgets:
		if isinstance(widget, pe.Button):
			widget.update(events)
	screen.fill((80,80,200))
	for item in widgets:
		item.draw_to(screen)
	pygame.display.flip()
	fpsclock.tick(fps)
