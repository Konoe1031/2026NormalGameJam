import pygame, random
import inventory, map, source, base, home, story, shop, bgm, hud, setting
from player import player_t
from hotkey import hotkey_t

pygame.init()
screen = pygame.display.set_mode((960, 720))
clock = pygame.time.Clock()
running = True
scene = "home"
inventory_open = False
previous_frame_tick = 0
pickup_sound = None
storage_sound = None

player = player_t()
bgm.play(bgm.MAIN_PAGE, 0.4)

def enter_game():
	global scene
	bgm.play(bgm.MAIN_GAME, 0.38)
	scene = "game"
def enter_bad_virus_ending():
	global scene
	story.load("bad_virus")
	bgm.play(bgm.BAD_END, 0.45)
	scene = "bad_ending"
def enter_bad_population_ending():
	global scene
	story.load("bad_population")
	bgm.play(bgm.BAD_END, 0.45)
	scene = "bad_ending"
def enter_bad_science_ending():
	global scene
	story.load("bad_science")
	bgm.play(bgm.BAD_END, 0.45)
	scene = "bad_ending"
def enter_bad_human_ending():
	global scene
	story.load("bad_human")
	bgm.play(bgm.BAD_END, 0.45)
	scene = "bad_ending"
def enter_bad_mutation_ending():
	global scene
	story.load("bad_mutation")
	bgm.play(bgm.BAD_END, 0.45)
	scene = "bad_ending"
def enter_real_ending():
	global scene
	story.load("real_end")
	bgm.play(bgm.REAL_END, 0.45)
	scene = "ending"
def enter_real2_ending():
	global scene
	story.load("real_end2")
	bgm.play(bgm.REAL_END, 0.45)
	scene = "ending"
def reached_escape_resources() -> bool:
	return base.resource["population"] > 50 and base.resource["metal"] > 50 and base.resource["plank"] > 50
def bought_all_upgrades_except_resistance() -> bool:
	for good, prices in setting.good_price.items():
		if good == "resistance":
			continue
		max_level = len(prices) - 1
		if player.upgrade.get(good, 0) < max_level:
			return False
	return True
def reached_real2_condition() -> bool:
	return bought_all_upgrades_except_resistance() and \
		player.upgrade.get("resistance", 0) == 0 and \
		base.resource["population"] >= 120
def check_interaction():
	global player, scene, pickup_sound, storage_sound
	biome = map.get_biome(player.x, player.y - 1, player)
	if biome == "home":
		if player.get_state() > 80 and random.uniform(0, 100) < 20:
			enter_bad_mutation_ending()
			return
		if storage_sound == None:
			if pygame.mixer.get_init():
				storage_sound = pygame.mixer.Sound("./src/audio/put_item.mp3")
		if storage_sound != None:
			storage_sound.play()
		base.store_resource()
	if biome == "shop":
		scene = "shop"
	for x, y in map.interactable:
		item = source.foreground_override[x, y]
		if not inventory.add_item(item):
			print("inventory is full")
			continue
		if pickup_sound == None:
			if pygame.mixer.get_init():
				pickup_sound = pygame.mixer.Sound("./src/audio/pickup.mp3")
		if pickup_sound != None:
			pickup_sound.play()
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
		elif scene == "home":
			if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				action = home.handle_click(event.pos)
				if action == "start":
					story.load("intro")
					bgm.play(bgm.CG, 0.45)
					scene = "story"
				elif action == "settings":
					scene = "settings"
		elif scene == "story":
			if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
				story.skip()
				enter_game()
				continue
			advance = (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1) or \
				(event.type == pygame.KEYDOWN and event.key in (pygame.K_SPACE, pygame.K_RETURN))
			if advance and story.advance():
				enter_game()
		elif scene == "bad_ending" or scene == "ending":
			advance = (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1) or \
				(event.type == pygame.KEYDOWN and event.key in (pygame.K_SPACE, pygame.K_RETURN))
			if advance and story.advance():
				player = player_t()
				bgm.play(bgm.MAIN_PAGE, 0.4)
				scene = "home"
		elif scene == "settings":
			if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				if home.handle_settings_click(event.pos) == "back":
					scene = "home"
					bgm.play(bgm.MAIN_PAGE, 0.4)
		elif scene == "game":
			if event.type == pygame.KEYDOWN:
				for keys in hotkeys.values():
					keys.check_down(event.key)
			if event.type == pygame.KEYUP:
				for keys in hotkeys.values():
					keys.check_up(event.key)
		elif scene == "shop":
			if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				action = shop.handle_click(event.pos)
				if action == "back":
					scene = "game"
					for hotkey in hotkeys.values():
						hotkey.press = False
				else:
					shop.buy(player, action)
	if scene == "game":
		if player.get_state() > 100:
			enter_bad_virus_ending()
			continue
		if base.resource["population"] < 2:
			enter_bad_population_ending()
			continue
		if reached_real2_condition():
			enter_real2_ending()
			continue
		if reached_escape_resources():
			if base.resource["science"] > 70:
				enter_bad_human_ending()
			else:
				enter_bad_science_ending()
			continue
		current_frame_tick = pygame.time.get_ticks() // 3000
		if previous_frame_tick < current_frame_tick:
			previous_frame_tick = current_frame_tick
			base.tick()
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
		map.draw_background(screen, player)
		map.draw_foreground(screen, player)
		map.draw_blind_mask(screen, player)
		hud.draw_player_state(screen, player)
		if inventory_open:
			inventory.draw(screen)
			base.draw_info(screen)
		map.draw_virus_flash(screen)
	elif scene == "shop":
		map.draw_background(screen, player)
		map.draw_foreground(screen, player)
		shop.draw(screen, player)
	elif scene == "home":
		home.draw(screen)
	elif scene == "story":
		story.draw(screen)
	elif scene == "bad_ending":
		story.draw(screen)
	elif scene == "ending":
		story.draw(screen)
	elif scene == "settings":
		home.draw_settings(screen)
	# Display
	pygame.display.flip()
	clock.tick(60)
pygame.quit()
