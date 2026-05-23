import pygame, random
import source, map, setting

class player_t:
	def __init__(self):
		self.image = source.load_source("girl", 2)
		# the position of the feet
		self.x = 0
		self.y = 0
		self.touch_distance = 1
		self.state = 100
		self.cooldown = 0
		self.speed_base = .125
	def move(self, x: float, y: float):
		self.cooldown -= 1
		if self.cooldown > pygame.time.get_ticks():
			return self
		if pygame.time.get_ticks() - self.cooldown > 5000: # 5 sec
			movability = self.state - setting.player_state["movability"]
			if movability > 0 and random.uniform(0, 100) < movability:
				self.cooldown = pygame.time.get_ticks() + 500
			else: self.cooldown = pygame.time.get_ticks()
		# target position
		tx, ty = self.x + x, self.y + y
		item = map.get_foreground_item(tx // 1, ty // 1, self)
		if item != None:
			return self
		biome = map.get_biome(tx // 1, ty // 1, self)
		if biome in ("ocean", "void"):
			return self
		self.x, self.y = tx, ty
		return self
	def speed(self):
		base = self.speed_base
		if self.state >= setting.player_state["upsidedown"]:
			base = -base
		if self.state >= setting.player_state["unstable"]:
			random.seed(f"unstable({pygame.time.get_ticks() // 100})")
			return random.uniform(.25, 1) * base
		return base
	def draw(self, screen: pygame.Surface):
		x = (screen.get_width() - self.image.get_width()) / 2
		y = (screen.get_height() + setting.tile_size) / 2 - self.image.get_height()
		screen.blit(self.image, (x, y))
		return self
