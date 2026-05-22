import pygame
import map

pygame.init()
screen = pygame.display.set_mode((960, 720))
clock = pygame.time.Clock()
running = True

x = y = 0

while running:
	for event in pygame.event.get():
		# User press 'X'
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:	x -= .25
			if event.key == pygame.K_RIGHT:	x += .25
			if event.key == pygame.K_UP:	y -= .25
			if event.key == pygame.K_DOWN:	y += .25
			print(x,y)
	# Game
	map.draw_background(screen, (x, y))
	# Display
	pygame.display.flip()
	clock.tick(60)
pygame.quit()
