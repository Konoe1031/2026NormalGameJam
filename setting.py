import json
import os
import pygame

# === 既有：遊戲狀態門檻（保留不動）===
player_state = {
	"unstable": 20,
	"movability": 30,
	"void": 40,
	"upsidedown": 75
}

# === 可調設定的預設值 ===
DEFAULTS = {
	"sfx_volume": 1.0,
	"music_volume": 1.0,
	"configured_seed": "9",
	"tile_size": 48,
	"typing_speed": 15,
	"key_inventory": pygame.K_TAB,
	"key_settings": pygame.K_ESCAPE,
}

# 會被持久化的可設定欄位（不變量：DEFAULTS 的每個鍵都會寫入 settings.json）
_PERSIST_KEYS = list(DEFAULTS.keys())

# 模組層設定值（初始化為預設）
sfx_volume = DEFAULTS["sfx_volume"]
music_volume = DEFAULTS["music_volume"]
configured_seed = DEFAULTS["configured_seed"]
tile_size = DEFAULTS["tile_size"]
typing_speed = DEFAULTS["typing_speed"]
key_inventory = DEFAULTS["key_inventory"]
key_settings = DEFAULTS["key_settings"]

# 使用中種子（map.py 讀取）。開新遊戲時由 configured_seed 複製而來
seed = configured_seed

SETTINGS_PATH = os.path.join(os.path.dirname(__file__), "settings.json")

# 已註冊、需隨 sfx_volume 調整的 Sound 物件
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
	"""登記一個音效 Sound，使其音量隨 sfx_volume 變動。"""
	if sound not in _sfx_sounds:
		_sfx_sounds.append(sound)
	sound.set_volume(sfx_volume)


def apply_audio() -> None:
	"""把目前音量套到 music 通道與所有已註冊音效。"""
	if pygame.mixer.get_init():
		pygame.mixer.music.set_volume(music_volume)
	for sound in _sfx_sounds:
		sound.set_volume(sfx_volume)
