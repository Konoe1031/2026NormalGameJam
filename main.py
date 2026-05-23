import pygame
import inventory, map, source, base
from player import player_t
from hotkey import hotkey_t

pygame.init()
screen = pygame.display.set_mode((960, 720))
clock = pygame.time.Clock()
running = True
inventory_open = False

player = player_t()

def check_interaction():
	global player
	if map.get_biome(player.x, player.y - 1, player) == "home":
		base.store_resource()
	for x, y in map.interactable:
		item = source.foreground_override[x, y]
		if not inventory.add_item(item):
			print("inventory is full")
			continue
		source.foreground_override[x, y] = f"empty_{item}"
	return
def open_inventory():
	global inventory_open
	inventory_open = True
	return
def close_inventory():
	global inventory_open
	inventory_open = False
	return

hotkeys: dict[str, hotkey_t] = {
	"move_left": hotkey_t([pygame.K_LEFT, pygame.K_a]),
	"move_right": hotkey_t([pygame.K_RIGHT, pygame.K_d]),
	"move_up": hotkey_t([pygame.K_UP, pygame.K_w]),
	"move_down": hotkey_t([pygame.K_DOWN, pygame.K_s]),
	"interaction": hotkey_t([pygame.K_e], on_down=check_interaction),
	"inventory": hotkey_t([pygame.K_TAB], on_down=open_inventory, on_up=close_inventory),
	"prevent": hotkey_t([pygame.K_LSHIFT, pygame.K_RSHIFT])
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
	player.action = None
	if hotkeys["prevent"].pressed():
		player.action = "prevent"
	if hotkeys["move_left"].pressed():
		player.move(-player.speed(), 0)
	if hotkeys["move_right"].pressed():
		player.move(player.speed(), 0)
	if hotkeys["move_up"].pressed():
		player.move(0, -player.speed())
	if hotkeys["move_down"].pressed():
		player.move(0, player.speed())
	# Game
	map.draw_background(screen, player)
	map.draw_foreground(screen, player)
	if inventory_open:
		inventory.draw(screen)
		base.draw_info(screen)
	# Display
	pygame.display.flip()
	clock.tick(60)
pygame.quit()
