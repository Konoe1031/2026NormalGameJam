import pygame
import inventory, map, source, home, story
from player import player_t
from hotkey import hotkey_t

pygame.init()
screen = pygame.display.set_mode((960, 720))
clock = pygame.time.Clock()
running = True
scene = "home"  # "home" | "game" | "settings"
inventory_open = False

player = player_t()
def check_interaction():
	for x, y in map.interactable:
		item = source.foreground_override[x, y]
		if not inventory.add_item(item):
			print("inventory is full")
			continue
		source.foreground_override[x, y] = f"empty_{item}"
		print(f"you've got a {item}")
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
	"inventory": hotkey_t([pygame.K_TAB], on_down=open_inventory, on_up=close_inventory)
}

while running:
	for event in pygame.event.get():
		# User press 'X'
		if event.type == pygame.QUIT:
			running = False
		elif scene == "home":
			if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				action = home.handle_click(event.pos)
				if action == "start":
					story.load("intro")
					scene = "story"
				elif action == "settings":
					scene = "settings"
		elif scene == "story":
			advance = (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1) or \
				(event.type == pygame.KEYDOWN and event.key in (pygame.K_SPACE, pygame.K_RETURN))
			if advance and story.advance():
				scene = "game"
		elif scene == "settings":
			if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				if home.handle_settings_click(event.pos) == "back":
					scene = "home"
		elif scene == "game":
			if event.type == pygame.KEYDOWN:
				for keys in hotkeys.values():
					keys.check_down(event.key)
			if event.type == pygame.KEYUP:
				for keys in hotkeys.values():
					keys.check_up(event.key)
					
	if scene == "game":
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
		if inventory_open:
			inventory.draw(screen)
	elif scene == "home":
		home.draw(screen)
	elif scene == "story":
		story.draw(screen)
	elif scene == "settings":
		home.draw_settings(screen)
	# Display
	pygame.display.flip()
	clock.tick(60)
pygame.quit()
