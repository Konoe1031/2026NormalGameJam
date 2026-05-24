import os
import pygame
import setting

MAIN_PAGE = "./src/bgm/mainpage_tunetank-piano-classical-music-348133.mp3"
CG = "./src/bgm/cg_konten_kreator-echoes-of-home-414068.mp3"
MAIN_GAME = "./src/bgm/maingame_tunetank-cinematic-ambient-348342.mp3"
BAD_END = "./src/bgm/badend_tunetank-classical-piano-background-347547.mp3"
REAL_END = "./src/bgm/realend_andriig-emotional-emotional-music-497354.mp3"

_current: str | None = None
_volume: float = 0.45


def _ensure_init() -> bool:
	if not pygame.mixer.get_init():
		try:
			pygame.mixer.init()
		except pygame.error as e:
			print(f"bgm: mixer init failed: {e}")
			return False
	return True


def play(path: str, volume: float = 0.45):
	global _current, _volume
	if _current == path:
		return
	if not _ensure_init():
		return
	if not os.path.exists(path):
		print(f"bgm: file not found: {path}")
		return
	try:
		pygame.mixer.music.load(path)
	except pygame.error as e:
		print(f"bgm: failed to load {path}: {e}")
		return
	_current = path
	_volume = volume
	pygame.mixer.music.set_volume(volume * setting.music_volume)
	pygame.mixer.music.play(loops=-1, fade_ms=800)


def apply_volume():
	if pygame.mixer.get_init():
		pygame.mixer.music.set_volume(_volume * setting.music_volume)


def stop():
	global _current
	if pygame.mixer.get_init():
		pygame.mixer.music.fadeout(800)
	_current = None
