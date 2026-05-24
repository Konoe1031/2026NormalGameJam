import os
import pygame
import setting

WIDTH, HEIGHT = 960, 720
FONT_PATH = os.path.join(os.path.dirname(__file__), "src", "fonts", "NotoSansTC.ttf")
SKIP_KEY = pygame.K_h

_STEPS = [
	{"signal": "move", "text": "用 WASD 或方向鍵移動"},
	{"signal": "pickup", "text": "走到發光的物件旁，按 E 撿取"},
	{"signal": "inventory", "text": "按 TAB 打開背包查看物品"},
	{"signal": "shop", "text": "走到商店建築旁，按 E 進入商店"},
	{"signal": "settings", "text": "點左上角齒輪可開啟設定"},
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
	_started = False
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
