import pygame
import random
import math
import setting, source, player
from typing import Tuple

def get_background_tile(x: float, y: float) -> pygame.Surface:
	random.seed(f"bgtile({x},{y},{setting.seed})")
	rand = random.randint(1, source.background_dict["grass"]) - 1
	return source.background["grass"][rand]
def get_foreground_item(x: float, y: float) -> pygame.Surface | None:
	random.seed(f"fgitem({x},{y},{setting.seed})")
	full = 99
	for item in source.foreground_dict["grass"].keys():
		if random.randint(0,full) < source.foreground_dict["grass"][item]:
			return source.foreground["grass"][item]
		full -= source.foreground_dict["grass"][item]
	return None

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
def draw_foreground(screen: pygame.Surface, player: player.player_t):
	item = source.foreground["grass"]["mango_tree"]
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
			item = get_foreground_item(ix, iy)
			if item != None:
				y = dy - item.get_height() + setting.tile_size
				screen.blit(item, (dx, y))
			dx += setting.tile_size
			ix += 1
		dy += setting.tile_size
		iy += 1
	player.draw(screen)
	while dy < screen.get_height():
		dx = -(px % setting.tile_size)
		ix = (px + dx) // setting.tile_size
		while dx < screen.get_width():
			item = get_foreground_item(ix, iy)
			if item != None:
				y = dy - item.get_height() + setting.tile_size
				screen.blit(item, (dx, y))
			dx += setting.tile_size
			ix += 1
		dy += setting.tile_size
		iy += 1