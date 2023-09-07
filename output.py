import pygame
import sys
import Pygame_Engine as pe

pygame.init()
screen = pygame.display.set_mode((500, 500))
fpsclock = pygame.time.Clock()
fps = 60

widgets = [
	pe.Label(None, "Entity positions (count: 2)", 22, (0, 0), "topleft", tc=[250, 250, 250], bgc=[40, 40, 40], force_width=500, force_height=30),
	pe.Label(None, "Pascal", 22, (0, 30), "topleft", tc=[250, 250, 250], bgc=[40, 40, 40], force_width=150, force_height=30),
	pe.Label(None, "(1, 1)", 22, (150, 30), "topleft", tc=[250, 250, 250], bgc=[40, 40, 40], force_width=150, force_height=30),
	pe.Button(None, "Change", 22, (300, 30), "topleft", tc=[250, 250, 250], bgc=[40, 40, 40], force_width=100, force_height=30),
	pe.Button(None, "Delete", 22, (400, 30), "topleft", tc=[250, 250, 250], bgc=[40, 40, 40], force_width=100, force_height=30),
	pe.Label(None, "Marcel", 22, (0, 60), "topleft", tc=[250, 250, 250], bgc=[40, 40, 40], force_width=150, force_height=30),
	pe.Label(None, "(2, 2)", 22, (150, 60), "topleft", tc=[250, 250, 250], bgc=[40, 40, 40], force_width=150, force_height=30),
	pe.Button(None, "Change", 22, (300, 60), "topleft", tc=[250, 250, 250], bgc=[40, 40, 40], force_width=100, force_height=30),
	pe.Button(None, "Delete", 22, (400, 60), "topleft", tc=[250, 250, 250], bgc=[40, 40, 40], force_width=100, force_height=30),
	pe.Label(None, "no formatting here, right? (a = 1)", 22, (0, 90), "topleft", tc=[250, 250, 250], bgc=[40, 40, 40], force_width=500, force_height=30),
	pe.Label(None, "All entities started from position (0, 0)", 22, (0, 120), "topleft", tc=[250, 250, 250], bgc=[40, 40, 40], force_width=500, force_height=30),
]

while True:
	for e in pygame.event.get():
		if e.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
	screen.fill((80,80,200))
	for item in widgets:
		item.draw_to(screen)
	pygame.display.flip()
	fpsclock.tick(fps)
