import os
import pygame
import math
import setting
import source

X = 270
Y = 600
ICON_SIZE = 82
BAR_X = X + 72
BAR_Y = Y + 16
BAR_WIDTH = 320
BAR_HEIGHT = 46
MAX_STATE = 100

SETTINGS_ICON = os.path.join(os.path.dirname(__file__), "src", "img", "button", "setting_icon.png")
CLICK_SOUND = os.path.join(os.path.dirname(__file__), "src", "audio", "button.mp3")
SETTINGS_ICON_SCALE = 0.8
SETTINGS_ICON_POS = (16, 16)

_settings_btn = None
_click_sound = None
_click_loaded = False


def _ensure_settings_button():
	global _settings_btn
	if _settings_btn is not None:
		return
	img = pygame.image.load(SETTINGS_ICON).convert_alpha()
	img = pygame.transform.smoothscale(img, (round(img.get_width() * SETTINGS_ICON_SCALE), round(img.get_height() * SETTINGS_ICON_SCALE)))
	vis = img.get_bounding_rect()
	rect = vis.copy()
	rect.topleft = SETTINGS_ICON_POS
	_settings_btn = {"img": img, "pos": (rect.x - vis.x, rect.y - vis.y), "rect": rect}


def _ensure_click():
	global _click_sound, _click_loaded
	if _click_loaded:
		return
	_click_loaded = True
	if not pygame.mixer.get_init():
		try:
			pygame.mixer.init()
		except pygame.error as e:
			print(f"hud: 音訊初始化失敗：{e}")
			return
	try:
		_click_sound = pygame.mixer.Sound(CLICK_SOUND)
		setting.register_sfx(_click_sound)
	except pygame.error as e:
		print(f"hud: 載入 {CLICK_SOUND} 失敗：{e}")


def draw_settings_button(screen: pygame.Surface):
	_ensure_settings_button()
	img, pos, rect = _settings_btn["img"], _settings_btn["pos"], _settings_btn["rect"]
	if rect.collidepoint(pygame.mouse.get_pos()):
		big = pygame.transform.smoothscale(img, (round(img.get_width() * 1.08), round(img.get_height() * 1.08)))
		screen.blit(big, big.get_rect(center=img.get_rect(topleft=pos).center))
	else:
		screen.blit(img, pos)


def settings_button_clicked(pos) -> bool:
	_ensure_settings_button()
	if _settings_btn["rect"].collidepoint(pos):
		_ensure_click()
		if _click_sound is not None:
			_click_sound.play()
		return True
	return False


def _jitter_points(points: list[tuple[int, int]]) -> list[tuple[int, int]]:
	now = pygame.time.get_ticks() // 220
	result = []
	for index, (x, y) in enumerate(points):
		offset = ((now + index * 3) % 5) - 2
		result.append((x, y + offset))
	return result


def draw_player_state(screen: pygame.Surface, player):
	value = max(0, min(player.get_state(), MAX_STATE)) / MAX_STATE
	layer = pygame.Surface((BAR_X + BAR_WIDTH + 24, Y + ICON_SIZE + 12), pygame.SRCALPHA)

	jump_interval = 2800 - int((value ** 1.7) * 1300)
	if value >= .35:
		jump_interval -= 350
	if value >= .65:
		jump_interval -= 450
	if value >= .85:
		jump_interval -= 350
	jump_interval = max(450, jump_interval)
	jump_duration = 360
	jump_height = 5 + value * 11
	jump_phase = pygame.time.get_ticks() % jump_interval
	jump = 0
	if jump_phase < jump_duration:
		jump = -math.sin(math.pi * jump_phase / jump_duration) * jump_height
	icon = pygame.transform.smoothscale(source.virus_icon, (ICON_SIZE, ICON_SIZE))
	icon.set_alpha(245)
	layer.blit(icon, (X, Y + jump))

	fill_width = int(BAR_WIDTH * value)
	if fill_width > 0:
		fill_right = BAR_X + fill_width
		fill_top = _jitter_points([
			(BAR_X, BAR_Y + 3),
			(BAR_X + fill_width // 3, BAR_Y),
			(BAR_X + fill_width * 2 // 3, BAR_Y + 2),
			(fill_right, BAR_Y + 1)
		])
		fill_bottom = _jitter_points([
			(fill_right, BAR_Y + BAR_HEIGHT - 1),
			(BAR_X + fill_width * 2 // 3, BAR_Y + BAR_HEIGHT + 1),
			(BAR_X + fill_width // 3, BAR_Y + BAR_HEIGHT - 2),
			(BAR_X, BAR_Y + BAR_HEIGHT - 1)
		])
		pygame.draw.polygon(layer, (118, 238, 136, 190), fill_top + fill_bottom)

	top = _jitter_points([
		(BAR_X, BAR_Y),
		(BAR_X + BAR_WIDTH // 3, BAR_Y - 3),
		(BAR_X + BAR_WIDTH * 2 // 3, BAR_Y - 1),
		(BAR_X + BAR_WIDTH, BAR_Y - 4)
	])
	bottom = _jitter_points([
		(BAR_X, BAR_Y + BAR_HEIGHT),
		(BAR_X + BAR_WIDTH // 3, BAR_Y + BAR_HEIGHT + 4),
		(BAR_X + BAR_WIDTH * 2 // 3, BAR_Y + BAR_HEIGHT + 1),
		(BAR_X + BAR_WIDTH, BAR_Y + BAR_HEIGHT + 5)
	])
	right = _jitter_points([
		(BAR_X + BAR_WIDTH, BAR_Y - 4),
		(BAR_X + BAR_WIDTH + 4, BAR_Y + BAR_HEIGHT + 5)
	])

	pygame.draw.lines(layer, (30, 165, 72, 210), False, top, 4)
	pygame.draw.lines(layer, (30, 165, 72, 210), False, bottom, 4)
	pygame.draw.lines(layer, (30, 165, 72, 210), False, right, 4)

	if fill_width > 0:
		fill_edge = BAR_X + fill_width
		pygame.draw.line(layer, (66, 235, 104, 160), (fill_edge, BAR_Y + 4), (fill_edge, BAR_Y + BAR_HEIGHT - 4), 3)

	layer.set_alpha(225)
	screen.blit(layer, (0, 0))
