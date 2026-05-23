import pygame
import map, source
from player import player_t
from hotkey import hotkey_t
from typing import Tuple

pygame.init()
screen = pygame.display.set_mode((960, 720))
clock = pygame.time.Clock()
running = True

player = player_t()
def check_interaction():
	for x, y in map.interactable:
		item = source.foreground_override[x, y]
		source.foreground_override[x, y] = f"empty_{item}"
		print(f"you've got a {item}")
	return
hotkeys: dict[str, hotkey_t] = {
	"move_left": hotkey_t([pygame.K_LEFT, pygame.K_a]),
	"move_right": hotkey_t([pygame.K_RIGHT, pygame.K_d]),
	"move_up": hotkey_t([pygame.K_UP, pygame.K_w]),
	"move_down": hotkey_t([pygame.K_DOWN, pygame.K_s]),
	"interaction": hotkey_t([pygame.K_e], on_down=check_interaction)
}

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
