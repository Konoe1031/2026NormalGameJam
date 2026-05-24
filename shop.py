import pygame
import source, setting, base
from player import player_t
from home import _font, _click_sound, _play_click, _draw_button, BTN_SCALE, WIDTH, HEIGHT
back_btn: dict = None
goods: dict[str, dict] = {}

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
	global back_btn, goods, _click_sound
	if back_btn != None: return
	right_margin, bottom_margin, gap = 95, 60, 34
	back_btn = _place(pygame.image.load(f"./src/img/button/back.png").convert_alpha(),
					bottomright=(WIDTH - right_margin, HEIGHT - bottom_margin))
	dx = WIDTH * 7 / 32
	dy = HEIGHT * 3 / 16
	GOOD_SIZE = (WIDTH * 7 / 64, WIDTH * 7 / 64)
	restaurant = pygame.image.load(f"./src/img/texture/restaurant_upgrade.png")
	restaurant = pygame.transform.scale(restaurant, GOOD_SIZE).convert_alpha()
	restaurant = _place(restaurant, topleft=(dx, dy))
	dx += WIDTH * 4 / 16
	house = pygame.image.load(f"./src/img/texture/house_upgrade.png")
	house = pygame.transform.scale(house, GOOD_SIZE).convert_alpha()
	house = _place(house, topleft=(dx, dy))
	dx += WIDTH* 4 / 16
	lab = pygame.image.load(f"./src/img/texture/lab_upgrade.png")
	lab = pygame.transform.scale(lab, GOOD_SIZE).convert_alpha()
	lab = _place(lab, topleft=(dx, dy))
	dx = WIDTH * 7 / 32
	dy += HEIGHT * 6 / 16
	distance = pygame.image.load(f"./src/img/texture/distance_upgrade.png")
	distance = pygame.transform.scale(distance, GOOD_SIZE).convert_alpha()
	distance = _place(distance, topleft=(dx, dy))
	dx += WIDTH * 4 / 16
	speed = pygame.image.load(f"./src/img/texture/speed_upgrade.png")
	speed = pygame.transform.scale(speed, GOOD_SIZE).convert_alpha()
	speed = _place(speed, topleft=(dx, dy))
	dx += WIDTH * 4 / 16
	resistance = pygame.image.load(f"./src/img/texture/resistance_upgrade.png")
	resistance = pygame.transform.scale(resistance, GOOD_SIZE).convert_alpha()
	resistance = _place(resistance, topleft=(dx, dy))
	goods = {
		"restaurant": restaurant, "lab": lab, "house": house,
		"distance": distance, "speed": speed, "resistance": resistance
	}
def handle_click(pos: tuple[int, int]) -> str | None:
	_ensure_init()
	if back_btn["rect"].collidepoint(pos):
		_play_click()
		return "back"
	for key, btn in goods.items():
		if btn["rect"].collidepoint(pos):
			_play_click()
			return key
	return None
def draw(screen: pygame.Surface, player: player_t):
	_ensure_init()
	_rect = ((WIDTH / 8, HEIGHT / 8), (WIDTH * 6 / 8, HEIGHT * 6 / 8))
	pygame.draw.rect(screen, (100, 100, 100), _rect)
	_draw_button(screen, back_btn)
	for key, btn in goods.items():
		level = player.upgrade.setdefault(key, 0)
		price = setting.good_price.get(key, [None])[level]
		if price == None: continue
		_draw_button(screen, btn)
		dx, dy = btn["rect"][0] - WIDTH / 32, btn["rect"][1]
		for key, cost in price.items():
			base.__draw_info(screen, source.resource[key], f"{cost}", dx, dy)
			dy += source.resource[key].get_height()


def buy(player: player_t, good: str):
	level = player.upgrade.setdefault(good, 0)
	price = setting.good_price.get(good, [None])[level]
	if price == None: return
	for kind, cost in price.items():
		if base.resource.get(kind, 0) < cost:
			return
	player.upgrade[good] += 1
	for kind, cost in price.items():
		base.resource[kind] -= cost
	if good == "distance":
		player.touch_distance += .5
	elif good == "speed":
		player.speed_base += .075
	elif good == "restaurant":
		base.food_decrease_ratio += 5
	elif good == "house":
		base.population_limit += 30
	return