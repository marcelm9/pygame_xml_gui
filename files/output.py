import pygame
import sys
import Pygame_Engine as pe

pygame.init()
screen = pygame.display.set_mode((500, 500))
fpsclock = pygame.time.Clock()
fps = 60
pygame.display.set_caption('Mockup')

widgets = [
	pe.Label(None, "New shift added", 22, (0, 0), "topleft", tc=[250, 250, 250], bgc=[40, 40, 40], hl=1, br=4, padding=2, force_width=500, force_height=30),
	pe.Label(None, "Type", 22, (0, 30), "topleft", tc=[250, 250, 250], bgc=[40, 40, 40], hl=1, br=4, padding=2, force_width=150, force_height=30),
	pe.Label(None, "KTW-RF", 22, (150, 30), "topleft", tc=[250, 250, 250], bgc=[40, 40, 40], hl=1, br=4, padding=2, force_width=350, force_height=30),
	pe.Label(None, "Car", 22, (0, 60), "topleft", tc=[250, 250, 250], bgc=[40, 40, 40], hl=1, br=4, padding=2, force_width=150, force_height=30),
	pe.Label(None, "A-39", 22, (150, 60), "topleft", tc=[250, 250, 250], bgc=[40, 40, 40], hl=1, br=4, padding=2, force_width=350, force_height=30),
	pe.Label(None, "Crew", 22, (0, 90), "topleft", tc=[250, 250, 250], bgc=[40, 40, 40], hl=1, br=4, padding=2, force_width=150, force_height=30),
	pe.Label(None, "Marcel Menzel", 22, (150, 90), "topleft", tc=[250, 250, 250], bgc=[40, 40, 40], hl=1, br=4, padding=2, force_width=350, force_height=30),
	pe.Label(None, "", 22, (0, 120), "topleft", tc=[250, 250, 250], bgc=[40, 40, 40], hl=1, br=4, padding=2, force_width=150, force_height=30),
	pe.Label(None, "Schuller Denis", 22, (150, 120), "topleft", tc=[250, 250, 250], bgc=[40, 40, 40], hl=1, br=4, padding=2, force_width=350, force_height=30),
	pe.Label(None, "Start", 22, (0, 150), "topleft", tc=[250, 250, 250], bgc=[40, 40, 40], hl=1, br=4, padding=2, force_width=150, force_height=30),
	pe.Label(None, "09.10.2023, 10:00", 22, (150, 150), "topleft", tc=[250, 250, 250], bgc=[40, 40, 40], hl=1, br=4, padding=2, force_width=350, force_height=30),
	pe.Label(None, "End", 22, (0, 180), "topleft", tc=[250, 250, 250], bgc=[40, 40, 40], hl=1, br=4, padding=2, force_width=150, force_height=30),
	pe.Label(None, "09.10.2023, 18:30", 22, (150, 180), "topleft", tc=[250, 250, 250], bgc=[40, 40, 40], hl=1, br=4, padding=2, force_width=350, force_height=30),
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
