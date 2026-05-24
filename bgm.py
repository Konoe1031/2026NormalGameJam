import os
import pygame

MAIN_PAGE = "./src/bgm/mainpage_tunetank-piano-classical-music-348133.mp3"
CG = "./src/bgm/cg_konten_kreator-echoes-of-home-414068.mp3"
MAIN_GAME = "./src/bgm/maingame_tunetank-cinematic-ambient-348342.mp3"
BAD_END = "./src/bgm/badend_tunetank-classical-piano-background-347547.mp3"
REAL_END = "./src/bgm/realend_andriig-emotional-emotional-music-497354.mp3"

_channel: pygame.mixer.Channel | None = None
_sounds: dict[str, pygame.mixer.Sound] = {}
_current: str | None = None


def _ensure_init() -> bool:
	global _channel
	if not pygame.mixer.get_init():
		try:
			pygame.mixer.init()
		except pygame.error as e:
			print(f"bgm: mixer init failed: {e}")
			return False
	if _channel == None:
		_channel = pygame.mixer.Channel(1)
	return True


def _load(path: str) -> pygame.mixer.Sound | None:
	if path in _sounds:
		return _sounds[path]
	if not os.path.exists(path):
		print(f"bgm: file not found: {path}")
		return None
	try:
		_sounds[path] = pygame.mixer.Sound(path)
		return _sounds[path]
	except pygame.error as e:
		print(f"bgm: failed to load {path}: {e}")
		return None


def play(path: str, volume: float = 0.45):
	global _current
	if _current == path:
		return
	if not _ensure_init():
		return
	sound = _load(path)
	if sound == None:
		return
	_current = path
	sound.set_volume(volume)
	_channel.fadeout(500)
	_channel.play(sound, loops=-1, fade_ms=800)


def stop():
	global _current
	if _channel != None:
		_channel.fadeout(800)
	_current = None
