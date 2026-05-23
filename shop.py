import pygame
import source, setting, base
from player import player_t
from home import _font, _click_sound, _play_click, _draw_button, BTN_SCALE, WIDTH, HEIGHT
_buttons: dict[str, dict] = {}

def _place(img: pygame.Surface, **anchor) -> dict:
	# img = 
	img = pygame.transform.smoothscale(img, (round(img.get_width() * BTN_SCALE), round(img.get_height() * BTN_SCALE)))
	vis = img.get_bounding_rect()
	screen_rect = vis.copy()
	for edge, value in anchor.items():
		setattr(screen_rect, edge, value)
	pos = (screen_rect.x - vis.x, screen_rect.y - vis.y)
	return {"img": img, "pos": pos, "rect": screen_rect}
def _ensure_init():
	global _buttons, _click_sound
	if _buttons.get("back") != None: return
	right_margin, bottom_margin, gap = 95, 60, 34
	back = _place(pygame.image.load(f"./src/img/button/back.png").convert_alpha(),
					bottomright=(WIDTH - right_margin, HEIGHT - bottom_margin))
	distance = _place(source.load_source("distance_upgrade", 2).convert_alpha(),
					bottomright=(WIDTH * 5 / 16, HEIGHT * 3 / 8))
	_buttons = {"back": back, "distance": distance}
def handle_click(pos: tuple[int, int]) -> str | None:
	_ensure_init()
	for key, btn in _buttons.items():
		if btn["rect"].collidepoint(pos):
			_play_click()
			return key
	return None
def draw(screen: pygame.Surface):
	_ensure_init()
	_rect = ((WIDTH / 8, HEIGHT / 8), (WIDTH * 6 / 8, HEIGHT * 6 / 8))
	pygame.draw.rect(screen, (100, 100, 100), _rect)
	for btn in _buttons.values():
		_draw_button(screen, btn)

def buy(player: player_t, good: str):
	price = setting.good_price.get(good)
	if price == None: return
	for kind, cost in price.items():
		if base.resource.get(kind, 0) < cost:
			return
	for kind, cost in price.items():
		base.resource[kind] -= cost
	if good == "distance":
		player.touch_distance += .5
		for kind, cost in price.items():
			setting.good_price[good][kind] += 5
	return