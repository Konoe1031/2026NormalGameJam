import pygame
import random
import setting, source, player
from typing import Tuple

home_position = (0, -1)

def is_home_position(x: int, y: int) -> bool:
	home = source.structures["home"]
	width = (home.get_width() + setting.tile_size - 1) // setting.tile_size
	height = (home.get_height() + setting.tile_size - 1) // setting.tile_size
	home_x, home_y = home_position
	return home_x <= int(x) < home_x + width and home_y - height + 1 <= int(y) <= home_y

def get_biome(x: int, y: int) -> str:
	if is_home_position(x, y):
		return "home"
	random.seed(f"biome({int(x)},{int(y)},{setting.seed})")
	distance = abs(x + y + random.randint(-1, 1))
	if distance < 50:
		return "grass"
	if distance < 150:
		return "clay"
	if distance < 200:
		return "lake"
	return "ocean"
def get_background_tile(x: int, y: int) -> pygame.Surface:
	biome = get_biome(x, y)
	if biome == "home":
		biome = "grass"
	random.seed(f"bgtile({int(x)},{int(y)},{setting.seed})")
	rand = random.randint(1, source.background_dict[biome]) - 1
	return source.background[biome][rand]
def get_foreground_item_name(x: int, y: int) -> Tuple[str, str | None]:
	biome = get_biome(x, y)
	if biome == "home":
		return biome, None
	override = source.foreground_override.setdefault((x, y), None)
	if override != None:
		return biome, override
	random.seed(f"fgitem({int(x)},{int(y)},{setting.seed})")
	full = 100
	if biome not in source.foreground_dict.keys():
		return biome, None
	for item in source.foreground_dict[biome].keys():
		requirement = source.foreground_dict[biome][item]["chance"]
		if requirement <= 0:
			continue
		if random.uniform(0, full) < requirement:
			if source.foreground_dict[biome][item]["source"]:
				source.foreground_override[x, y] = item
			return biome, item
		full -= requirement
	return biome, None
def get_foreground_item(x: int, y: int) -> pygame.Surface | None:
	biome, name = get_foreground_item_name(x, y)
	if name == None:
		return None
	if name in source.structures:
		return source.structures[name]
	return source.foreground[biome].setdefault(name, None)

def draw_background(screen: pygame.Surface, player: player.player_t):
	tile = source.background["grass"][0]
	# pivot position (the left right corner)
	px = player.x * setting.tile_size - screen.get_width() / 2
	py = player.y * setting.tile_size - screen.get_height() / 2
	# delta position (the left right corner of the current tile)
	dy = -(py % setting.tile_size)
	# integer position (the integer position of the current tile)
	iy = (py + dy) // setting.tile_size
	while dy < screen.get_height():
		dx = -(px % setting.tile_size)
		ix = (px + dx) // setting.tile_size
		while dx < screen.get_width():
			tile = get_background_tile(ix, iy)
			screen.blit(tile, (dx, dy))
			dx += setting.tile_size
			ix += 1
		dy += setting.tile_size
		iy += 1
interactable: list[Tuple[int, int]] = []
def __get_screen_position(screen: pygame.Surface, player: player.player_t, x: int, y: int) -> Tuple[float, float]:
	px = player.x * setting.tile_size - screen.get_width() / 2
	py = player.y * setting.tile_size - screen.get_height() / 2
	return x * setting.tile_size - px, y * setting.tile_size - py

def __draw_home(screen: pygame.Surface, player: player.player_t):
	home = source.structures["home"]
	home_x, home_y = home_position
	x, tile_y = __get_screen_position(screen, player, home_x, home_y)
	y = tile_y - home.get_height() + setting.tile_size
	if x > screen.get_width() or x + home.get_width() < 0:
		return
	if y > screen.get_height() or y + home.get_height() < 0:
		return
	screen.blit(home, (x, y))

def __draw_foreground(screen: pygame.Surface, player: player.player_t, ix: int, iy: int, dx: float, dy: float):
	item = get_foreground_item(ix, iy)
	if item == None:
		return
	y = dy - item.get_height() + setting.tile_size
	screen.blit(item, (dx, y))
	biome, name = get_foreground_item_name(ix, iy)
	item_setting = source.foreground_dict.get(biome, {}).get(name)
	if item_setting != None and item_setting["source"] and\
		abs(ix - player.x + .5) + abs(iy - player.y + .5) <= player.touch_distance:
		screen.blit(source.hints["e"], (dx, dy))
		interactable.append((ix, iy))
	return
def draw_foreground(screen: pygame.Surface, player: player.player_t):
	interactable.clear()
	__draw_home(screen, player)
	# pivot position (the left right corner)
	px = player.x * setting.tile_size - screen.get_width() / 2
	py = player.y * setting.tile_size - screen.get_height() / 2
	# delta position (the left right corner of the current tile)
	dy = -(py % setting.tile_size)
	# integer position (the integer position of the current tile)
	iy = (py + dy) // setting.tile_size
	while dy < screen.get_height() / 2:
		dx = -(px % setting.tile_size)
		ix = (px + dx) // setting.tile_size
		while dx < screen.get_width():
			__draw_foreground(screen, player, ix, iy, dx, dy)
			dx += setting.tile_size
			ix += 1
		dy += setting.tile_size
		iy += 1
	player.draw(screen)
	while dy < screen.get_height():
		dx = -(px % setting.tile_size)
		ix = (px + dx) // setting.tile_size
		while dx < screen.get_width():
			__draw_foreground(screen, player, ix, iy, dx, dy)
			dx += setting.tile_size
			ix += 1
		dy += setting.tile_size
		iy += 1
