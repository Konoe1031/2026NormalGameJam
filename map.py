import pygame
import random
import math
import os
from typing import Tuple

tile_size = 48

def load_source(path: str, scale: int = 1) -> pygame.Surface:
	img: pygame.Surface = None
	for kind in ("jpg", "png", "jpeg"):
		file = f"./texture/{path}.{kind}"
		if os.path.exists(file):
			img = pygame.image.load(file)
			break
	factor = max(scale, 1) * tile_size / min(img.get_width(), img.get_height())
	return pygame.transform.scale(img, (img.get_width() * factor, img.get_height() * factor))

# [type of land][number of variant]
background_source_dict = {"grass": 2, "ocean": 1}
background_source: dict[str, list[pygame.Surface]] = {}
for land, count in background_source_dict.items():
	background_source[land] = []
	for i in range(count):
		background_source[land].append(load_source(f"{land}{i}"))
# [type of land][type of item][chance %]
foreground_source_dict = {
	"grass": {"mango_tree": 1}
}
foreground_source: dict[str, dict[str, pygame.Surface]] = {}
for land, content in foreground_source_dict.items():
	foreground_source[land] = {}
	for item in content.keys():
		foreground_source[land][item] = load_source(f"{land}_{item}")

def get_background_tile(x: int, y: int) -> pygame.Surface:
	random.seed(f"bgtile({x},{y})")
	rand = random.randint(1, background_source_dict["grass"]) - 1
	return background_source["grass"][rand]
def get_foreground_item(x: int, y: int) -> pygame.Surface | None:
	random.seed(f"fgitem({x},{y})")
	full = 99
	for item in foreground_source_dict["grass"].keys():
		if random.randint(0,full) < foreground_source_dict["grass"][item]:
			return foreground_source["grass"][item]
		full -= foreground_source_dict["grass"][item]
	return None

def draw_background(screen: pygame.Surface, player_position: Tuple[float, float]):
	tile = background_source["grass"][0]
	# pivot position (the left right corner)
	px = player_position[0] * tile_size - screen.get_width() / 2
	py = player_position[1] * tile_size - screen.get_height() / 2
	# delta position (the left right corner of the current tile)
	dx = math.floor(px / tile_size) * tile_size - px
	# integer position (the integer position of the current tile)
	ix = (px + dx) // tile_size
	while dx < screen.get_width():
		dy = math.floor(py / tile_size) * tile_size - py
		iy = (py + dy) // tile_size
		while dy < screen.get_height():
			tile = get_background_tile(ix, iy)
			screen.blit(tile, (dx, dy))
			dy += tile_size
			iy += 1
		dx += tile_size
		ix += 1

def draw_foreground(screen: pygame.Surface, player_position: Tuple[float, float]):
	item = foreground_source["grass"]["mango_tree"]
	# pivot position (the left right corner)
	px = player_position[0] * tile_size - screen.get_width() / 2
	py = player_position[1] * tile_size - screen.get_height() / 2
	# delta position (the left right corner of the current tile)
	dx = math.floor(px / tile_size) * tile_size - px
	# integer position (the integer position of the current tile)
	ix = (px + dx) // tile_size
	while dx < screen.get_width():
		dy = math.floor(py / tile_size) * tile_size - py
		iy = (py + dy) // tile_size
		while dy < screen.get_height():
			item = get_foreground_item(ix, iy)
			if item != None:
				screen.blit(item, (dx - item.get_width() + tile_size, dy - item.get_height() + tile_size))
			dy += tile_size
			iy += 1
		dx += tile_size
		ix += 1