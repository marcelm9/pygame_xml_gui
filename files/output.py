import pygame
import sys
import Pygame_Engine as pe

pygame.init()
screen = pygame.display.set_mode((500, 500))
fpsclock = pygame.time.Clock()
fps = 60

widgets = [
	pe.Label(None, "Entity positions (count: 8)", 22, (0, 0), "topleft", tc=[250, 250, 250], bgc=[40, 40, 40], hl=1, br=4, padding=2, force_width=500, force_height=30),
	pe.Label(None, "Pascal", 22, (0, 30), "topleft", tc=[250, 250, 250], bgc=[40, 40, 40], hl=1, br=4, padding=2, force_width=150, force_height=30),
	pe.Label(None, "(1, 1)", 22, (150, 30), "topleft", tc=[250, 250, 250], bgc=[40, 40, 40], hl=1, br=4, padding=2, force_width=50, force_height=30),
	pe.Button(None, "Change", 22, (200, 30), "topleft", tc=[250, 250, 250], bgc=[40, 40, 40], hl=1, br=4, padding=2, force_width=100, force_height=30),
	pe.Button(None, "Round", 22, (300, 30), "topleft", tc=[250, 250, 250], bgc=[40, 40, 40], hl=1, br=4, padding=2, force_width=100, force_height=30),
	pe.Button(None, "Delete", 22, (400, 30), "topleft", tc=[250, 250, 250], bgc=(200, 40, 40), hl=1, br=4, padding=2, force_width=100, force_height=30),
	pe.Label(None, "Marcel", 22, (0, 60), "topleft", tc=[250, 250, 250], bgc=[40, 40, 40], hl=1, br=4, padding=2, force_width=150, force_height=30),
	pe.Label(None, "(2, 2)", 22, (150, 60), "topleft", tc=[250, 250, 250], bgc=[40, 40, 40], hl=1, br=4, padding=2, force_width=50, force_height=30),
	pe.Button(None, "Change", 22, (200, 60), "topleft", tc=[250, 250, 250], bgc=[40, 40, 40], hl=1, br=4, padding=2, force_width=100, force_height=30),
	pe.Button(None, "Round", 22, (300, 60), "topleft", tc=[250, 250, 250], bgc=[40, 40, 40], hl=1, br=4, padding=2, force_width=100, force_height=30),
	pe.Button(None, "Delete", 22, (400, 60), "topleft", tc=[250, 250, 250], bgc=(200, 40, 40), hl=1, br=4, padding=2, force_width=100, force_height=30),
	pe.Label(None, "Lena", 22, (0, 90), "topleft", tc=[250, 250, 250], bgc=[40, 40, 40], hl=1, br=4, padding=2, force_width=150, force_height=30),
	pe.Label(None, "(3, 3)", 22, (150, 90), "topleft", tc=[250, 250, 250], bgc=[40, 40, 40], hl=1, br=4, padding=2, force_width=50, force_height=30),
	pe.Button(None, "Change", 22, (200, 90), "topleft", tc=[250, 250, 250], bgc=[40, 40, 40], hl=1, br=4, padding=2, force_width=100, force_height=30),
	pe.Button(None, "Round", 22, (300, 90), "topleft", tc=[250, 250, 250], bgc=[40, 40, 40], hl=1, br=4, padding=2, force_width=100, force_height=30),
	pe.Button(None, "Delete", 22, (400, 90), "topleft", tc=[250, 250, 250], bgc=(200, 40, 40), hl=1, br=4, padding=2, force_width=100, force_height=30),
	pe.Label(None, "Nahee", 22, (0, 120), "topleft", tc=[250, 250, 250], bgc=[40, 40, 40], hl=1, br=4, padding=2, force_width=150, force_height=30),
	pe.Label(None, "(4, 4)", 22, (150, 120), "topleft", tc=[250, 250, 250], bgc=[40, 40, 40], hl=1, br=4, padding=2, force_width=50, force_height=30),
	pe.Button(None, "Change", 22, (200, 120), "topleft", tc=[250, 250, 250], bgc=[40, 40, 40], hl=1, br=4, padding=2, force_width=100, force_height=30),
	pe.Button(None, "Round", 22, (300, 120), "topleft", tc=[250, 250, 250], bgc=[40, 40, 40], hl=1, br=4, padding=2, force_width=100, force_height=30),
	pe.Button(None, "Delete", 22, (400, 120), "topleft", tc=[250, 250, 250], bgc=(200, 40, 40), hl=1, br=4, padding=2, force_width=100, force_height=30),
	pe.Label(None, "Benni", 22, (0, 150), "topleft", tc=[250, 250, 250], bgc=[40, 40, 40], hl=1, br=4, padding=2, force_width=150, force_height=30),
	pe.Label(None, "(5, 5)", 22, (150, 150), "topleft", tc=[250, 250, 250], bgc=[40, 40, 40], hl=1, br=4, padding=2, force_width=50, force_height=30),
	pe.Button(None, "Change", 22, (200, 150), "topleft", tc=[250, 250, 250], bgc=[40, 40, 40], hl=1, br=4, padding=2, force_width=100, force_height=30),
	pe.Button(None, "Round", 22, (300, 150), "topleft", tc=[250, 250, 250], bgc=[40, 40, 40], hl=1, br=4, padding=2, force_width=100, force_height=30),
	pe.Button(None, "Delete", 22, (400, 150), "topleft", tc=[250, 250, 250], bgc=(200, 40, 40), hl=1, br=4, padding=2, force_width=100, force_height=30),
	pe.Label(None, "Amelie", 22, (0, 180), "topleft", tc=[250, 250, 250], bgc=[40, 40, 40], hl=1, br=4, padding=2, force_width=150, force_height=30),
	pe.Label(None, "(6, 6)", 22, (150, 180), "topleft", tc=[250, 250, 250], bgc=[40, 40, 40], hl=1, br=4, padding=2, force_width=50, force_height=30),
	pe.Button(None, "Change", 22, (200, 180), "topleft", tc=[250, 250, 250], bgc=[40, 40, 40], hl=1, br=4, padding=2, force_width=100, force_height=30),
	pe.Button(None, "Round", 22, (300, 180), "topleft", tc=[250, 250, 250], bgc=[40, 40, 40], hl=1, br=4, padding=2, force_width=100, force_height=30),
	pe.Button(None, "Delete", 22, (400, 180), "topleft", tc=[250, 250, 250], bgc=(200, 40, 40), hl=1, br=4, padding=2, force_width=100, force_height=30),
	pe.Label(None, "Laurenz", 22, (0, 210), "topleft", tc=[250, 250, 250], bgc=[40, 40, 40], hl=1, br=4, padding=2, force_width=150, force_height=30),
	pe.Label(None, "(7, 7)", 22, (150, 210), "topleft", tc=[250, 250, 250], bgc=[40, 40, 40], hl=1, br=4, padding=2, force_width=50, force_height=30),
	pe.Button(None, "Change", 22, (200, 210), "topleft", tc=[250, 250, 250], bgc=[40, 40, 40], hl=1, br=4, padding=2, force_width=100, force_height=30),
	pe.Button(None, "Round", 22, (300, 210), "topleft", tc=[250, 250, 250], bgc=[40, 40, 40], hl=1, br=4, padding=2, force_width=100, force_height=30),
	pe.Button(None, "Delete", 22, (400, 210), "topleft", tc=[250, 250, 250], bgc=(200, 40, 40), hl=1, br=4, padding=2, force_width=100, force_height=30),
	pe.Label(None, "Anni", 22, (0, 240), "topleft", tc=[250, 250, 250], bgc=[40, 40, 40], hl=1, br=4, padding=2, force_width=150, force_height=30),
	pe.Label(None, "(8, 8)", 22, (150, 240), "topleft", tc=[250, 250, 250], bgc=[40, 40, 40], hl=1, br=4, padding=2, force_width=50, force_height=30),
	pe.Button(None, "Change", 22, (200, 240), "topleft", tc=[250, 250, 250], bgc=[40, 40, 40], hl=1, br=4, padding=2, force_width=100, force_height=30),
	pe.Button(None, "Round", 22, (300, 240), "topleft", tc=[250, 250, 250], bgc=[40, 40, 40], hl=1, br=4, padding=2, force_width=100, force_height=30),
	pe.Button(None, "Delete", 22, (400, 240), "topleft", tc=[250, 250, 250], bgc=(200, 40, 40), hl=1, br=4, padding=2, force_width=100, force_height=30),
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
