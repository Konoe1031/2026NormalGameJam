import pygame, math
import inventory, setting, source
_font: pygame.font.Font = None

INITIAL_POPULATION_LIMIT = 30.1
INITIAL_FOOD_DECREASE_RATIO = 10
INITIAL_RESOURCE = {
	"food": 20,
	"population": 10,
	"metal": 0,
	"plank": 0,
	"science": 0
	}
population_limit = INITIAL_POPULATION_LIMIT
food_decrease_ratio = INITIAL_FOOD_DECREASE_RATIO
resource = INITIAL_RESOURCE.copy()
resource_value = {
	"metal": {"metal": 1},
	"plank": {"plank": 1},
	"bone": {"science": 1},
	"drug": {"science": 3},
	"mango": {"food": 5},
	"can": {"food": 8},
	"meat": {"food": 15},
	"good_meat": {"food": 1, "science": .5},
	"cake": {"food": 3, "population": 1}
}

def reset():
	global population_limit, food_decrease_ratio, resource
	population_limit = INITIAL_POPULATION_LIMIT
	food_decrease_ratio = INITIAL_FOOD_DECREASE_RATIO
	resource = INITIAL_RESOURCE.copy()

def store_resource():
	global resource
	for i, slot in enumerate(inventory.slots):
		if slot == None: continue
		value = resource_value.get(slot["item"])
		for kind, num in value.items():
			resource[kind] += num * slot["count"]
		inventory.slots[i] = None
	return
def tick():
	global resource
	resource["food"] -= max(1, int(resource["population"] // food_decrease_ratio))
	if resource["food"] < 0:
		resource["population"] += resource["food"]
		resource["food"] = 0
	if resource["population"] < 0:
		resource["population"] = 0
		return
	if resource["food"] / resource["population"] > .5:
		resource["population"] += math.sqrt(resource["population"]) / 4
		if resource["population"] > population_limit:
			resource["population"] = population_limit
	return

def __render_text(text: str):
	global _font
	if _font == None:
		_font = pygame.font.SysFont(None, 48)
	return _font.render(text, True, 0)
def __draw_info(screen: pygame.Surface, icon: pygame.Surface, text: str, x: float, y: float):
	screen.blit(icon, (x - setting.tile_size, y - setting.tile_size / 4))
	screen.blit(__render_text(text), (x, y))
	return
def draw_info(screen: pygame.Surface):
	x = screen.get_width() - 2 * setting.tile_size
	y = setting.tile_size / 2
	for kind in ("food", "population", "metal", "plank", "science"):
		__draw_info(screen, source.resource[kind], f"{int(resource[kind])}", x, y)
		y += setting.tile_size
	return
