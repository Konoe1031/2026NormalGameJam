import pygame
import source, map, setting

class player_t:
	def __init__(self):
		self.image = source.load_source("girl", 2)
		# the position of the feet
		self.x = 0
		self.y = 0
		self.touch_distance = 1
	def move(self, x: float, y: float):
		# target position
		tx, ty = self.x + x, self.y + y
		item = map.get_foreground_item(tx // 1, ty // 1)
		if item != None:
			return self
		biome = map.get_biome(tx // 1, ty // 1)
		if biome == "ocean":
			return self
		self.x, self.y = tx, ty
		return self
	def draw(self, screen: pygame.Surface):
		x = (screen.get_width() - self.image.get_width()) / 2
		y = (screen.get_height() + setting.tile_size) / 2 - self.image.get_height()
		screen.blit(self.image, (x, y))
		return self
