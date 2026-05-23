import pygame, random
import source, map, setting

class player_t:
	def __init__(self, clock: pygame.time.Clock):
		self.image = source.load_source("girl", 2)
		self.clock = clock
		# the position of the feet
		self.x = 0
		self.y = 0
		self.touch_distance = 1
		self.state = 50
		self.cooldown = 0
	def move(self, x: float, y: float):
		self.cooldown -= 1
		if self.cooldown > 0:
			return self
		if self.cooldown < -self.clock.get_fps():
			movability = self.state - setting.player_state["movability"]
			if movability > 0 and random.uniform(0, 100) < movability:
				self.cooldown = self.clock.get_fps() / 2
			else: self.cooldown /= 3
		# target position
		tx, ty = self.x + x, self.y + y
		if self.state >= setting.player_state["upsidedown"]:
			tx, ty = self.x - x, self.y - y
		item = map.get_foreground_item(tx // 1, ty // 1, self)
		if item != None:
			return self
		biome = map.get_biome(tx // 1, ty // 1, self)
		if biome in ("ocean", "void"):
			return self
		self.x, self.y = tx, ty
		return self
	def draw(self, screen: pygame.Surface):
		x = (screen.get_width() - self.image.get_width()) / 2
		y = (screen.get_height() + setting.tile_size) / 2 - self.image.get_height()
		screen.blit(self.image, (x, y))
		return self
