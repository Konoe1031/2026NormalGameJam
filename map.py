import pygame
import random
import setting, source, player
from typing import Tuple

def get_biome(x: int, y: int) -> str:
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
	random.seed(f"bgtile({int(x)},{int(y)},{setting.seed})")
	rand = random.randint(1, source.background_dict[biome]) - 1
	return source.background[biome][rand]
def get_foreground_item_name(x: int, y: int) -> Tuple[str, str | None]:
	biome = get_biome(x, y)
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
	return source.foreground[biome][name]

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
def __draw_foreground(screen: pygame.Surface, player: player.player_t, ix: int, iy: int, dx: float, dy: float):
	item = get_foreground_item(ix, iy)
	if item == None:
		return
	y = dy - item.get_height() + setting.tile_size
	screen.blit(item, (dx, y))
	biome, name = get_foreground_item_name(ix, iy)
	if source.foreground_dict[biome][name]["source"] and\
		abs(ix - player.x + .5) + abs(iy - player.y + .5) <= player.touch_distance:
		screen.blit(source.hints["e"], (dx, y))
	return
def draw_foreground(screen: pygame.Surface, player: player.player_t):
	item: pygame.Surface = None
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
