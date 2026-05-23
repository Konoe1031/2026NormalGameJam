import pygame, math
import inventory, setting, source

food: int = 20
population: int = 10
metal: int = 0
plank: int = 0
science: int = 0
font: pygame.font.Font = None

def store_resource():
	global food, population, metal, plank, science
	for i, slot in enumerate(inventory.slots):
		if slot == None:
			continue
		if slot["item"] == "metal":
			metal += slot["count"]
		elif slot["item"] == "plank":
			plank += slot["count"]
		elif slot["item"] == "bone":
			science += slot["count"]
		elif slot["item"] == "drug":
			science += 3 * slot["count"]
		elif slot["item"] == "mango":
			food += 5 * slot["count"]
		elif slot["item"] == "can":
			food += 8 * slot["count"]
		elif slot["item"] == "meat":
			food += 12 * slot["count"]
		elif slot["item"] == "cake":
			food += 3 * slot["count"]
			population += slot["count"]
		inventory.slots[i] = None
	return
def tick():
	global food, population
	food -= max(1, int(population // 10))
	if food < 0:
		population += food
		food = 0
	if food / population > .5:
		population += math.sqrt(population) / 4
	return

def __draw_info(screen: pygame.Surface, icon: pygame.Surface, text: str, x: float, y: float):
	screen.blit(icon, (x - setting.tile_size, y - setting.tile_size / 4))
	screen.blit(font.render(text, True, 0), (x, y))
	return
def draw_info(screen: pygame.Surface):
	global food, population, metal, plank, science, font
	if font == None:
		font = pygame.font.SysFont(None, 48)
	x = screen.get_width() - 2 * setting.tile_size
	y = setting.tile_size / 2
	__draw_info(screen, source.foreground["clay"]["can"], f"{food}", x, y)
	y += setting.tile_size
	__draw_info(screen, source.population_icon, f"{int(population)}", x, y)
	y += setting.tile_size
	__draw_info(screen, source.foreground["grass"]["metal"], f"{metal}", x, y)
	y += setting.tile_size
	__draw_info(screen, source.foreground["grass"]["plank"], f"{plank}", x, y)
	y += setting.tile_size
	__draw_info(screen, source.foreground["clay"]["drug"], f"{science}", x, y)
	return
