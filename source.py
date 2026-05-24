import pygame
import setting
import os
from typing import Tuple

_image_cache: dict[str, pygame.Surface] = {}

def load_source(path: str, scale: float = 1) -> pygame.Surface:
	img: pygame.Surface = None
	for kind in ("jpg", "png", "jpeg"):
		file = f"./src/img/texture/{path}.{kind}"
		if file in _image_cache:
			img = _image_cache[file]
			break
		if os.path.exists(file):
			img = pygame.image.load(file)
			_image_cache[file] = img
			break
	factor = max(scale, 1) * setting.tile_size / min(img.get_width(), img.get_height())
	return pygame.transform.scale(img, (img.get_width() * factor, img.get_height() * factor))

background_dict = {
	"grass": 3,
	"clay": 3,
	"lake": 3,
	"ocean": 1,
	"void": 1
}
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

foreground_override: dict[Tuple[int, int], str] = {}

hints: dict[str, pygame.Surface] = {}
population_icon: pygame.Surface | None = None
virus_icon: pygame.Surface | None = None
structures: dict[str, pygame.Surface] = {}
background: dict[str, list[pygame.Surface]] = {}
foreground: dict[str, dict[str, pygame.Surface]] = {}
girl: dict[str, list[pygame.Surface]] = {}


def build() -> None:
	global hints, population_icon, virus_icon, structures, background, foreground, girl

	hints = {}
	for key in ("e",):
		hints[key] = load_source(f"hint_{key}")

	population_icon = load_source("population")
	virus_icon = load_source("virus")
	structures = {
		"home": load_source("home", 9)
	}

	# [type of land][number of variant]
	background = {}
	for land, count in background_dict.items():
		background[land] = []
		for i in range(count):
			background[land].append(load_source(f"{land}{i}"))

	# [type of land][type of item][chance %]
	foreground = {}
	for land, content in foreground_dict.items():
		foreground[land] = {}
		for item in content.keys():
			foreground[land][item] = load_source(f"{land}_{item}")

	# [facing][animation]
	girl = {
		"fallback": [load_source("girl", 2)],
		"left_prevent": [load_source("girl_vomit_1", 2)],
		"right_prevent": [load_source("girl_vomit_2", 2)],
		"left_stuck": [load_source("girl_left_prevent", 2)],
		"right_stuck": [load_source("girl_right_prevent", 2)],
		"up_walk": [load_source(f"girl_up_walk{i}", 2) for i in (0,1,0,2)],
		"down_walk": [load_source(f"girl_down_walk{i}", 2) for i in (0,1,0,2)],
		"left_walk": [load_source(f"girl_left_walk{i}", 2) for i in (0,1,0,2)],
		"right_walk": [load_source(f"girl_right_walk{i}", 2) for i in (0,1,0,2)]
	}


def rescale() -> None:
	build()


build()
