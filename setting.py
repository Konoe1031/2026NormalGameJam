import json
import os
import pygame

player_state = {
	"unstable": 20,
	"movability": 30,
	"void": 40,
	"upsidedown": 75
}

DEFAULTS = {
	"sfx_volume": 1.0,
	"music_volume": 1.0,
	"configured_seed": "9",
	"tile_size": 48,
	"typing_speed": 15,
	"key_inventory": pygame.K_TAB,
	"key_settings": pygame.K_ESCAPE,
}

_PERSIST_KEYS = list(DEFAULTS.keys())

sfx_volume = DEFAULTS["sfx_volume"]
music_volume = DEFAULTS["music_volume"]
configured_seed = DEFAULTS["configured_seed"]
tile_size = DEFAULTS["tile_size"]
typing_speed = DEFAULTS["typing_speed"]
key_inventory = DEFAULTS["key_inventory"]
key_settings = DEFAULTS["key_settings"]

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


def register_sfx(sound) -> None:
	if sound not in _sfx_sounds:
		_sfx_sounds.append(sound)
	sound.set_volume(sfx_volume)


def apply_audio() -> None:
	if pygame.mixer.get_init():
		pygame.mixer.music.set_volume(music_volume)
	for sound in _sfx_sounds:
		sound.set_volume(sfx_volume)
