import pygame
import setting
import os
from typing import Tuple

def load_source(path: str, scale: float = 1) -> pygame.Surface:
	img: pygame.Surface = None
	for kind in ("jpg", "png", "jpeg"):
		file = f"./src/img/texture/{path}.{kind}"
		if os.path.exists(file):
			img = pygame.image.load(file)
			break
	factor = max(scale, 1) * setting.tile_size / min(img.get_width(), img.get_height())
	return pygame.transform.scale(img, (img.get_width() * factor, img.get_height() * factor))

hints: dict[str, pygame.Surface] = {}
for key in ("e"):
	hints[key] = load_source(f"hint_{key}")

population_icon = load_source("population")
structures: dict[str, pygame.Surface] = {
	"home": load_source("home", 9)
}

background_dict = {
	"grass": 3,
	"clay": 3,
	"lake": 3,
	"ocean": 1,
	"void": 1
}
# [type of land][number of variant]
background: dict[str, list[pygame.Surface]] = {}
for land, count in background_dict.items():
	background[land] = []
	for i in range(count):
		background[land].append(load_source(f"{land}{i}"))

foreground_dict = {
	"grass": {
		"mango": {"chance": 0, "source": True},
		"mango_tree": {"chance": 1, "source": True},
		"empty_mango_tree": {"chance": 0, "source": False},
		"plank": {"chance": 1, "source": True},
		"metal": {"chance": .05, "source": True},
		"outlet": {"chance": .05, "source": False}
	},
	"clay": {
		"can": {"chance": .25, "source": True},
		"bone": {"chance": 1, "source": True},
		"metal": {"chance": .5, "source": True},
		"drug": {"chance": .1, "source": True},
		"outlet": {"chance": .25, "source": False}
	},
	"lake": {
		"metal": {"chance": .75, "source": True},
		"cake": {"chance": .5, "source": True},
		"drug": {"chance": .5, "source": True},
		"outlet": {"chance": 1, "source": False}
	}
}
# [type of land][type of item][chance %]
foreground: dict[str, dict[str, pygame.Surface]] = {}
for land, content in foreground_dict.items():
	foreground[land] = {}
	for item in content.keys():
		foreground[land][item] = load_source(f"{land}_{item}")
foreground_override: dict[Tuple[int, int], str] = {}

# [facing][animation]
girl: dict[str, list[pygame.Surface]] = {
	"fallback": [load_source("girl", 2)],
	"left_prevent": [load_source("girl_left_prevent", 2)],
	"right_prevent": [load_source("girl_right_prevent", 2)],
	"up_walk": [load_source(f"girl_up_walk{i}", 2) for i in (0,1,0,2)],
	"down_walk": [load_source(f"girl_down_walk{i}", 2) for i in (0,1,0,2)],
	"left_walk": [load_source(f"girl_left_walk{i}", 2) for i in (0,1,0,2)],
	"right_walk": [load_source(f"girl_right_walk{i}", 2) for i in (0,1,0,2)]
}
