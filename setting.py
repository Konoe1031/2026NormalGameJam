import json
import os
import pygame

home_position = (0, -1)
shop_position = (4, 3)
player_state = {
	"unstable": 20,
	"movability": 30,
	"blind": 40,
	"void": 60,
	"elmo": 70,
	"upsidedown": 80
}
good_price = {
	"distance": [{"metal": 5, "plank": 5}, {"metal": 10, "plank": 10}, {"metal": 10, "plank": 10}, None],
	"speed": [{"science": 5, "food": 5}, {"science": 15, "food": 10}, None],
	"restaurant": [{"plank": 5, "food": 5}, {"metal": 5, "food": 10}, {"science": 5, "food": 20}, {"science": 10, "food": 40}, None],
	"lab": [{"science": 5}, {"science": 10, "metal": 3}, {"science": 15, "food": 15}, None],
	"house": [{"plank": 10}, {"plank": 15, "metal": 5}, {"plank": 15, "science": 10}, None],
	"resistance": [None, {"population": 30}, None]
}

DEFAULTS = {
	"sfx_volume": 1.0,
	"music_volume": 1.0,
	"configured_seed": "9",
	"tile_size": 48,
	"typing_speed": 15,
	"key_inventory": pygame.K_TAB,
	"key_settings": pygame.K_ESCAPE,
	"key_prevent": pygame.K_LSHIFT,
}

_PERSIST_KEYS = list(DEFAULTS.keys())

sfx_volume = DEFAULTS["sfx_volume"]
music_volume = DEFAULTS["music_volume"]
configured_seed = DEFAULTS["configured_seed"]
tile_size = DEFAULTS["tile_size"]
typing_speed = DEFAULTS["typing_speed"]
key_inventory = DEFAULTS["key_inventory"]
key_settings = DEFAULTS["key_settings"]
key_prevent = DEFAULTS["key_prevent"]

seed = configured_seed

SETTINGS_PATH = os.path.join(os.path.dirname(__file__), "settings.json")

_sfx_sounds: list = []


def to_dict() -> dict:
	return {key: globals()[key] for key in _PERSIST_KEYS}


def load(path=SETTINGS_PATH) -> None:
	global seed
	data = {}
	try:
		with open(path, encoding="utf-8") as f:
			data = json.load(f)
	except (OSError, json.JSONDecodeError) as e:
		print(f"setting: 讀取 {path} 失敗，使用預設值：{e}")
	for key in _PERSIST_KEYS:
		globals()[key] = data.get(key, DEFAULTS[key])
	seed = configured_seed


def save(path=SETTINGS_PATH) -> None:
	try:
		with open(path, "w", encoding="utf-8") as f:
			json.dump(to_dict(), f, ensure_ascii=False, indent=2)
	except OSError as e:
		print(f"setting: 寫入 {path} 失敗：{e}")


def restore(data: dict) -> None:
	for key in _PERSIST_KEYS:
		if key in data:
			globals()[key] = data[key]
	apply_audio()


def register_sfx(sound) -> None:
	if sound not in _sfx_sounds:
		_sfx_sounds.append(sound)
	sound.set_volume(sfx_volume)


def apply_audio() -> None:
	if pygame.mixer.get_init():
		pygame.mixer.music.set_volume(music_volume)
	for sound in _sfx_sounds:
		sound.set_volume(sfx_volume)
