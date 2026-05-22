import pygame
import random
import math
from typing import Tuple

background_size = 48
background_source = dict[str, list[pygame.Surface]]()
background_source_dict = { "grass": 1, "ocean": 1 }
for type, count in background_source_dict.items():
	background_source[type] = [
		pygame.transform.scale(
			pygame.image.load(f"./texture/{type}{i}.jpg"),
			(background_size, background_size)
		) for i in range(count)
	]
def get_background_tile(x: int, y: int) -> pygame.Surface:
	random.seed(f"({x},{y})")
	rand = random.randint(1, background_source_dict["grass"]) - 1
	return background_source["grass"][rand]

def draw_background(screen: pygame.Surface, player_position: Tuple[float, float]):
	tile = background_source["grass"][0]
	px = player_position[0] * background_size - screen.get_width() / 2
	py = player_position[1] * background_size - screen.get_height() / 2
	dx = math.floor(px / background_size) * background_size - px
	while dx < screen.get_width():
		dy = math.floor(py / background_size) * background_size - py
		while dy < screen.get_height():
			tile = get_background_tile((px + dx) // background_size, (py + dy) // background_size)
			screen.blit(tile, (dx, dy))
			dy += tile.get_height()
		dx += tile.get_width()