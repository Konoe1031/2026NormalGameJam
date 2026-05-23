import pygame, math
import inventory, setting, source
_font: pygame.font.Font = None

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
	resource["food"] -= max(1, int(resource["population"] // 10))
	if resource["food"] < 0:
		resource["population"] += resource["food"]
		resource["food"] = 0
	if resource["food"] / resource["population"] > .5:
		resource["population"] += math.sqrt(resource["population"]) / 4
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
	__draw_info(screen, source.foreground["clay"]["can"], f"{resource['food']}", x, y)
	y += setting.tile_size
	__draw_info(screen, source.population_icon, f"{int(resource['population'])}", x, y)
	y += setting.tile_size
	__draw_info(screen, source.foreground["grass"]["metal"], f"{resource['metal']}", x, y)
	y += setting.tile_size
	__draw_info(screen, source.foreground["grass"]["plank"], f"{resource['plank']}", x, y)
	y += setting.tile_size
	__draw_info(screen, source.foreground["clay"]["drug"], f"{resource['science']}", x, y)
	return
