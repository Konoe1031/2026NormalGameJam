import pygame, math
import inventory, setting, source
_font: pygame.font.Font = None

population_limit = 30.1
food_decrease_ratio = 10
resource = {
	"food": 20,
	"population": 10,
	"metal": 0,
	"plank": 0,
	"science": 0
	}
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

def __draw_info(screen: pygame.Surface, icon: pygame.Surface, text: str, x: float, y: float):
	global _font
	if _font == None:
		_font = pygame.font.SysFont(None, 48)
	screen.blit(icon, (x - setting.tile_size, y - setting.tile_size / 4))
	screen.blit(_font.render(text, True, 0), (x, y))
	return
def draw_info(screen: pygame.Surface):
	x = screen.get_width() - 2 * setting.tile_size
	y = setting.tile_size / 2
	for kind in ("food", "population", "metal", "plank", "science"):
		__draw_info(screen, source.resource[kind], f"{int(resource[kind])}", x, y)
		y += setting.tile_size
	return
