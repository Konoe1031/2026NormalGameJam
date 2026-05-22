import pygame
import map

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

while running:
	for event in pygame.event.get():
		# User press 'X'
		if event.type == pygame.QUIT:
			running = False
	# Game
	map.draw_background(screen)
	# Display
	pygame.display.flip()
	clock.tick(60)
pygame.quit()
