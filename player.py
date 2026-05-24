import pygame, random
import source, map, setting

class player_t:
	def __init__(self):
		self.images = source.girl["fallback"]
		# the position of the feet
		self.x = 0
		self.y = 0
		self.facing = "down"
		self.touch_distance = 1
		self.state = 0
		self.cooldown = 0
		self.speed_base = .125
		self.action = None
		self.upgrade = {
			"distance": 0
		}
	def move(self, x: float, y: float):
		if y > 0: self.facing = "down"
		if y < 0: self.facing = "up"
		if x > 0: self.facing = "right"
		if x < 0: self.facing = "left"
		if self.action == "prevent":
			return self
		if self.cooldown > pygame.time.get_ticks():
			self.action = "stuck"
			return self
		if pygame.time.get_ticks() - self.cooldown > 5000: # 5 sec
			movability = self.state - setting.player_state["movability"]
			if movability > 0 and random.uniform(0, 100) < movability:
				self.cooldown = pygame.time.get_ticks() + 500
				self.action = "stuck"
				return self
			else: self.cooldown = pygame.time.get_ticks()
		# target position
		tx, ty = self.x + x, self.y + y
		item = map.get_foreground_item(tx // 1, ty // 1, self)
		if item != None:
			return self
		biome = map.get_biome(tx // 1, ty // 1, self)
		if biome in ("ocean", "home", "shop", "void"):
			return self
		self.action = "walk"
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
		self.images = None
		if self.action == "prevent":
			if self.facing in ("left", "down"):
				self.images = source.girl.get("left_prevent")
			else: self.images = source.girl.get("right_prevent")
		if self.action == "stuck":
			if self.facing in ("left", "down"):
				self.images = source.girl.get("left_stuck")
			else: self.images = source.girl.get("right_stuck")
		if self.action == "walk":
			self.images = source.girl.get(f"{self.facing}_walk")
		if self.images == None:
			self.images = source.girl["fallback"]
		image = self.images[pygame.time.get_ticks() // 250 % len(self.images)]
		x = (screen.get_width() - image.get_width()) / 2
		y = (screen.get_height() + setting.tile_size) / 2 - image.get_height()
		screen.blit(image , (x, y))
		return self
	
