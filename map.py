import pygame
import math
import random
import setting, source, inventory
from player import player_t
from typing import Tuple

virus_waves: list[dict] = []
virus_next_times: dict[Tuple[int, int], int] = {}
virus_speed = 0.12
virus_radius_max = 320
virus_width = 14
virus_damage = 5
virus_flash_until = 0
virus_flash_duration = 220
virus_wave_sound_path = "./src/audio/virus_wave.mp3"
virus_wave_sound: pygame.mixer.Sound | None = None
blind_mask_path = "./src/img/texture/mask.webp"
blind_mask: pygame.Surface | None = None
blind_mask_scaled: pygame.Surface | None = None
blind_mask_size: Tuple[int, int] | None = None

def __play_virus_wave_sound():
	global virus_wave_sound
	if not pygame.mixer.get_init():
		try:
			pygame.mixer.init()
		except pygame.error as e:
			print(f"virus_wave: mixer init failed: {e}")
			return
	if virus_wave_sound == None:
		try:
			virus_wave_sound = pygame.mixer.Sound(virus_wave_sound_path)
			virus_wave_sound.set_volume(0.75)
		except pygame.error as e:
			print(f"virus_wave: failed to load {virus_wave_sound_path}: {e}")
			return
	virus_wave_sound.play()

def draw_blind_mask(screen: pygame.Surface, player: player_t):
	global blind_mask, blind_mask_scaled, blind_mask_size
	if player.state < setting.player_state["blind"]:
		return
	if blind_mask == None:
		try:
			blind_mask = pygame.image.load(blind_mask_path).convert_alpha()
		except pygame.error as e:
			print(f"blind: failed to load {blind_mask_path}: {e}")
			return
	screen_size = screen.get_size()
	if blind_mask_scaled == None or blind_mask_size != screen_size:
		blind_mask_scaled = pygame.transform.smoothscale(blind_mask, screen_size)
		blind_mask_size = screen_size
	screen.blit(blind_mask_scaled, (0, 0))

def __next_virus_time(x: int, y: int, now: int) -> int:
	rng = random.Random(f"virus_next({int(x)},{int(y)},{now},{setting.seed})")
	return now + rng.randint(2500, 6500)

def is_home_position(x: int, y: int) -> bool:
	home = source.structures["home"]
	width = (home.get_width() + setting.tile_size - 1) // setting.tile_size
	height = (home.get_height() + setting.tile_size - 1) // setting.tile_size
	home_x, home_y = setting.home_position
	return home_x <= int(x) < home_x + width and home_y - height + 1 <= int(y) <= home_y
def is_shop_position(x: int, y: int) -> bool:
	home = source.structures["shop"]
	width = (home.get_width() + setting.tile_size - 1) // setting.tile_size
	height = (home.get_height() + setting.tile_size - 1) // setting.tile_size
	home_x, home_y = setting.shop_position
	return home_x <= int(x) < home_x + width and home_y - height + 1 <= int(y) <= home_y

def get_biome(x: int, y: int, player: player_t) -> str:
	x //= 1; y //= 1
	if is_home_position(x, y):
		return "home"
	if is_shop_position(x, y):
		return "shop"
	if (player.x // 1 != x or player.y // 1 != y) and player.state >= setting.player_state["void"]:
		random.seed(f"void({int(x)},{int(y)},{setting.seed})")
		if random.uniform(0, 100) < 1:
			return "void"
	random.seed(f"biome({int(x)},{int(y)},{setting.seed})")
	distance = abs(x + random.randint(-1, 1)) + abs(y + random.randint(-1, 1))
	if distance < 75:
		return "grass"
	if distance < 150:
		return "clay"
	if distance < 200:
		return "lake"
	return "ocean"
def get_background_tile(x: int, y: int, player: player_t) -> pygame.Surface:
	biome = get_biome(x, y, player)
	if biome in ("home", "shop"): biome = "grass"
	random.seed(f"bgtile({int(x)},{int(y)},{setting.seed})")
	rand = random.randint(1, source.background_dict[biome]) - 1
	return source.background[biome][rand]
def get_foreground_item_name(x: int, y: int, player: player_t) -> Tuple[str, str | None]:
	biome = get_biome(x, y, player)
	if biome in ("home", "shop"):
		return biome, None
	if biome not in source.foreground_dict:
		return biome, None
	override = source.foreground_override.get((x, y))
	if override != None:
		return biome, override
	random.seed(f"fgitem({int(x)},{int(y)},{setting.seed})")
	full = 100
	for item in source.foreground_dict[biome].keys():
		requirement = source.foreground_dict[biome][item]["chance"]
		if requirement <= 0:
			continue
		if random.uniform(0, full) < requirement:
			if source.foreground_dict[biome][item]["source"]:
				source.foreground_override[x, y] = item
			return biome, item
		full -= requirement
	return biome, None
def get_foreground_item(x: int, y: int, player: player_t) -> pygame.Surface | None:
	biome, name = get_foreground_item_name(x, y, player)
	if name == None:
		return None
	if name in source.structures:
		return source.structures[name]
	return source.foreground.get(biome, {}).get(name)

def draw_background(screen: pygame.Surface, player: player_t):
	tile = source.background["grass"][0]
	# pivot position (the left right corner)
	px = player.x * setting.tile_size - screen.get_width() / 2
	py = player.y * setting.tile_size - screen.get_height() / 2
	# delta position (the left right corner of the current tile)
	dy = -(py % setting.tile_size)
	# integer position (the integer position of the current tile)
	iy = (py + dy) // setting.tile_size
	while dy < screen.get_height():
		dx = -(px % setting.tile_size)
		ix = (px + dx) // setting.tile_size
		while dx < screen.get_width():
			tile = get_background_tile(ix, iy, player)
			screen.blit(tile, (dx, dy))
			dx += setting.tile_size
			ix += 1
		dy += setting.tile_size
		iy += 1
interactable: list[Tuple[int, int]] = []
def __get_screen_position(screen: pygame.Surface, player: player_t, x: int, y: int) -> Tuple[float, float]:
	px = player.x * setting.tile_size - screen.get_width() / 2
	py = player.y * setting.tile_size - screen.get_height() / 2
	return x * setting.tile_size - px, y * setting.tile_size - py
def __draw_home(screen: pygame.Surface, player: player_t):
	home = source.structures["home"]
	home_x, home_y = setting.home_position
	x, tile_y = __get_screen_position(screen, player, home_x, home_y)
	y = tile_y - home.get_height() + setting.tile_size
	if x > screen.get_width() or x + home.get_width() < 0:
		return
	if y > screen.get_height() or y + home.get_height() < 0:
		return
	screen.blit(home, (x, y))
def __draw_shop(screen: pygame.Surface, player: player_t):
	home = source.structures["shop"]
	home_x, home_y = setting.shop_position
	x, tile_y = __get_screen_position(screen, player, home_x, home_y)
	y = tile_y - home.get_height() + setting.tile_size
	if x > screen.get_width() or x + home.get_width() < 0:
		return
	if y > screen.get_height() or y + home.get_height() < 0:
		return
	screen.blit(home, (x, y))
def __update_virus_outlet(ix: int, iy: int):
	now = pygame.time.get_ticks()
	key = (int(ix), int(iy))
	next_time = virus_next_times.setdefault(key, __next_virus_time(ix, iy, now))
	if now < next_time:
		return
	virus_waves.append({
		"x": int(ix),
		"y": int(iy),
		"start": now,
		"hit": False
	})
	virus_next_times[key] = __next_virus_time(ix, iy, now)

def __draw_virus_waves(screen: pygame.Surface, player: player_t):
	global virus_flash_until
	now = pygame.time.get_ticks()
	active_waves = []
	for wave in virus_waves:
		age = now - wave["start"]
		radius = age * virus_speed
		if radius > virus_radius_max:
			continue
		x, y = __get_screen_position(screen, player, wave["x"], wave["y"])
		center = (int(x + setting.tile_size / 2), int(y + setting.tile_size / 2))
		pygame.draw.circle(screen, (80, 255, 110), center, int(radius), virus_width)
		pygame.draw.circle(screen, (20, 120, 45), center, int(radius), 2)
		dx = (player.x - (wave["x"] + .5)) * setting.tile_size
		dy = (player.y - (wave["y"] + .5)) * setting.tile_size
		distance = math.sqrt(dx * dx + dy * dy)
		if not wave["hit"] and abs(distance - radius) <= virus_width:
			if player.action != "prevent":
				player.state += virus_damage
				virus_flash_until = now + virus_flash_duration
				__play_virus_wave_sound()
				print(f"infected: state={player.state}")
			wave["hit"] = True
		active_waves.append(wave)
	virus_waves[:] = active_waves

def draw_virus_flash(screen: pygame.Surface):
	now = pygame.time.get_ticks()
	if now >= virus_flash_until:
		return
	progress = (virus_flash_until - now) / virus_flash_duration
	alpha = int(210 * progress)
	flash = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
	flash.fill((43, 186, 74, alpha))
	screen.blit(flash, (0, 0))

def __draw_foreground(screen: pygame.Surface, player: player_t, ix: int, iy: int, dx: float, dy: float):
	item = get_foreground_item(ix, iy, player)
	if item == None:
		return
	y = dy - item.get_height() + setting.tile_size
	screen.blit(item, (dx, y))
	biome, name = get_foreground_item_name(ix, iy, player)
	if( biome == "clay" or biome == "grass")and name == "outlet":
		__update_virus_outlet(ix, iy)
	item_setting = source.foreground_dict.get(biome, {}).get(name)
	if item_setting != None and item_setting["source"] and\
		abs(ix - player.x + .5) + abs(iy - player.y + .5) <= player.touch_distance:
		screen.blit(source.hints["e"], (dx, dy))
		interactable.append((ix, iy))
	return
def draw_foreground(screen: pygame.Surface, player: player_t):
	interactable.clear()
	__draw_home(screen, player)
	__draw_shop(screen, player)
	# pivot position (the left right corner)
	px = player.x * setting.tile_size - screen.get_width() / 2
	py = player.y * setting.tile_size - screen.get_height() / 2
	# delta position (the left right corner of the current tile)
	dy = -(py % setting.tile_size)
	# integer position (the integer position of the current tile)
	iy = (py + dy) // setting.tile_size
	while dy < screen.get_height() / 2:
		dx = -(px % setting.tile_size)
		ix = (px + dx) // setting.tile_size
		while dx < screen.get_width():
			__draw_foreground(screen, player, ix, iy, dx, dy)
			dx += setting.tile_size
			ix += 1
		dy += setting.tile_size
		iy += 1
	__draw_virus_waves(screen, player)
	if get_biome(player.x, player.y - 1, player) == "home" and inventory.slots[0] != None:
		screen.blit(source.hints["e"], ((screen.get_width() - setting.tile_size) / 2, (screen.get_height() - 5 * setting.tile_size) / 2))
	if get_biome(player.x, player.y - 1, player) == "shop":
		screen.blit(source.hints["e"], ((screen.get_width() - setting.tile_size) / 2, (screen.get_height() - 5 * setting.tile_size) / 2))
	player.draw(screen)
	while dy < screen.get_height():
		dx = -(px % setting.tile_size)
		ix = (px + dx) // setting.tile_size
		while dx < screen.get_width():
			__draw_foreground(screen, player, ix, iy, dx, dy)
			dx += setting.tile_size
			ix += 1
		dy += setting.tile_size
		iy += 1
