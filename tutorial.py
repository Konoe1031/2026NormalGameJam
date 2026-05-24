import os
import pygame
import setting

WIDTH, HEIGHT = 960, 720
FONT_PATH = os.path.join(os.path.dirname(__file__), "src", "fonts", "NotoSansTC.ttf")
SKIP_KEY = pygame.K_h

_STEPS = [
	{"signal": "move", "text": "用 WASD 或方向鍵移動看看，按下 shift 可以屏氣躲避毒氣"},
	{"signal": "pickup", "text": "靠近任何一個物件，按 E 撿取看看"},
	{"signal": "inventory", "text": "按 TAB 打開背包：中央是攜帶物，右上角是倉庫，可把撿拾的物品放進"},
	{"signal": "store", "text": "回倉庫旁按 E 把東西存進倉庫，可以在商店裡用倉庫裡的東西升級"},
	{"signal": "shop", "text": "走到商店旁按 E，可以在這裡升級基地和自己本身"},
	{"signal": "settings", "text": "點左上角的齒輪可以打開設定"},
]

_index = 0
_started = False
_origin = (0.0, 0.0)
_events: set = set()
_font: pygame.font.Font = None
_hint_font: pygame.font.Font = None


def start(player):
	global _index, _started, _origin, _events
	_index = 0
	_started = True
	_origin = (player.x, player.y)
	_events = set()


def active() -> bool:
	return _started and _index < len(_STEPS)


def notify(event: str):
	_events.add(event)


def _finish():
	global _started
	#_started = False
	setting.tutorial_done = True
	setting.save()


def _step_done(player) -> bool:
	signal = _STEPS[_index]["signal"]
	if signal == "move":
		return abs(player.x - _origin[0]) + abs(player.y - _origin[1]) > 1
	return signal in _events


def update(player):
	global _index
	if not active():
		return
	while _index < len(_STEPS) and _step_done(player):
		_index += 1
	if _index >= len(_STEPS):
		_finish()


def try_skip(key) -> bool:
	if key == SKIP_KEY and active():
		_finish()
		return True
	return False


def _cjk_font(size: int) -> pygame.font.Font:
	if os.path.exists(FONT_PATH):
		return pygame.font.Font(FONT_PATH, size)
	return pygame.font.SysFont(None, size)


def _ensure_fonts():
	global _font, _hint_font
	if _font is None:
		_font = _cjk_font(28)
		_hint_font = _cjk_font(20)


def draw(screen: pygame.Surface):
	if not active():
		return
	_ensure_fonts()
	box_h = 60
	top = HEIGHT - 195
	box = pygame.Surface((WIDTH, box_h), pygame.SRCALPHA)
	box.fill((20, 20, 20, 180))
	screen.blit(box, (0, top))
	text = _STEPS[_index]["text"]
	screen.blit(_font.render(text, True, (245, 245, 245)), (40, top + 16))
	hint = _hint_font.render("按 H 跳過教學", True, (200, 200, 200))
	screen.blit(hint, hint.get_rect(bottomright=(WIDTH - 24, top + box_h - 8)))
