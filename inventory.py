import pygame
import source

ROWS = 3
COLUMNS = 5
SLOT_COUNT = ROWS * COLUMNS
SLOT_SIZE = 48
SLOT_GAP = 8
PADDING = 16
MAX_STACK = 7

slots: list[dict[str, str | int] | None] = [None] * SLOT_COUNT

def reset():
	global slots
	slots = [None] * SLOT_COUNT

def add_item(item: str) -> bool:
	if item == "mango_tree":
		item = "mango"
	if item in ("elmo", "omuba"):
		item = "good_meat"
	for slot in slots:
		if slot != None and slot["item"] == item and slot["count"] < MAX_STACK:
			slot["count"] += 1
			return True
	for index, slot in enumerate(slots):
		if slot == None:
			slots[index] = {"item": item, "count": 1}
			return True
	return False

def get_item_image(item: str) -> pygame.Surface | None:
	for biome_items in source.foreground.values():
		if item in biome_items:
			return biome_items[item]
	return None

def draw(screen: pygame.Surface):
	width = COLUMNS * SLOT_SIZE + (COLUMNS - 1) * SLOT_GAP
	height = ROWS * SLOT_SIZE + (ROWS - 1) * SLOT_GAP
	panel_width = width + PADDING * 2
	panel_height = height + PADDING * 2
	panel_x = (screen.get_width() - panel_width) / 2
	panel_y = (screen.get_height() - panel_height) / 2

	panel = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
	panel.fill((20, 24, 32, 180))
	screen.blit(panel, (panel_x, panel_y))

	slot_image = pygame.transform.scale(source.background["lake"][1], (SLOT_SIZE, SLOT_SIZE))
	for row in range(ROWS):
		for column in range(COLUMNS):
			index = row * COLUMNS + column
			x = panel_x + PADDING + column * (SLOT_SIZE + SLOT_GAP)
			y = panel_y + PADDING + row * (SLOT_SIZE + SLOT_GAP)
			screen.blit(slot_image, (x, y))
			pygame.draw.rect(screen, (230, 240, 255), (x, y, SLOT_SIZE, SLOT_SIZE), 2)

			slot = slots[index]
			if slot == None:
				continue
			item_image = get_item_image(str(slot["item"]))
			if item_image != None:
				item_image = pygame.transform.scale(item_image, (SLOT_SIZE, SLOT_SIZE))
				screen.blit(item_image, (x, y))
			if slot["count"] > 1:
				font = pygame.font.Font(None, 24)
				text = font.render(str(slot["count"]), True, (255, 255, 255))
				text_rect = text.get_rect(bottomright=(x + SLOT_SIZE - 4, y + SLOT_SIZE - 2))
				screen.blit(text, text_rect)
