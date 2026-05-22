import pygame
import map, player
from hotkey import hotkey_t
from typing import Tuple

pygame.init()
screen = pygame.display.set_mode((960, 720))
clock = pygame.time.Clock()
running = True

hotkeys: dict[str, hotkey_t] = {
	"move_left": hotkey_t([pygame.K_LEFT, pygame.K_a]),
	"move_right": hotkey_t([ pygame.K_RIGHT, pygame.K_d ]),
	"move_up": hotkey_t([ pygame.K_UP, pygame.K_w ]),
	"move_down": hotkey_t([ pygame.K_DOWN, pygame.K_s ])
}
player = player.player_t()

while running:
	for event in pygame.event.get():
		# User press 'X'
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.KEYDOWN:
			for keys in hotkeys.values():
				keys.check_down(event.key)
		if event.type == pygame.KEYUP:
			for keys in hotkeys.values():
				keys.check_up(event.key)
	if hotkeys["move_left"].pressed():
		player.move(-.125, 0)
	if hotkeys["move_right"].pressed():
		player.move(.125, 0)
	if hotkeys["move_up"].pressed():
		player.move(0, -.125)
	if hotkeys["move_down"].pressed():
		player.move(0, .125)
	# Game
	map.draw_background(screen, player)
	map.draw_foreground(screen, player)
	# Display
	pygame.display.flip()
	clock.tick(60)
pygame.quit()
