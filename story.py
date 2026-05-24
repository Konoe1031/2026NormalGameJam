import json
import os
import pygame
import setting

WIDTH, HEIGHT = 960, 720
BOX_H = 200
PAD = 40
TYPING_SOUND = "./src/audio/typing.mp3"
SOUND_START = 1.0  # 從音檔第幾秒開始播（跳過開頭靜音）
FONT_PATH = os.path.join(os.path.dirname(__file__), "src", "fonts", "NotoSansTC.ttf")

_font: pygame.font.Font = None
_hint_font: pygame.font.Font = None
_cg_cache: dict[str, pygame.Surface] = {}
_beats: list[dict[str, str]] = []
_index = 0
_typed = 0.0
_last_ms: int | None = None
_audio_ok = False
_sound_on = False


def _cjk_font(size: int) -> pygame.font.Font:
	if os.path.exists(FONT_PATH):
		return pygame.font.Font(FONT_PATH, size)
	for name in ("stheitimedium", "arialunicode", "hiraginosansgb", "applesdgothicneo",
	             "microsoftjhenghei", "microsoftyahei", "notosanscjktc"):
		path = pygame.font.match_font(name)
		if path:
			return pygame.font.Font(path, size)
	return pygame.font.SysFont(None, size)


def _ensure_init() -> None:
	global _font, _hint_font, _audio_ok
	if _font is not None:
		return
	_font = _cjk_font(32)
	_hint_font = _cjk_font(24)
	if not pygame.mixer.get_init():
		try:
			pygame.mixer.init()
		except pygame.error as e:
			print(f"story: 音訊初始化失敗，劇情將無音效：{e}")
	_audio_ok = pygame.mixer.get_init() is not None
	if _audio_ok:
		try:
			pygame.mixer.music.load(TYPING_SOUND)
		except pygame.error as e:
			print(f"story: 載入 {TYPING_SOUND} 失敗，劇情將無音效：{e}")
			_audio_ok = False


def load(script: str = "intro") -> None:
	global _beats, _index
	with open(f"./src/script/{script}.json", encoding="utf-8") as f:
		_beats = json.load(f)
	_index = 0
	_reset_typing()


def _reset_typing() -> None:
	global _typed, _last_ms
	_typed = 0.0
	_last_ms = None


def _update_typing(text: str) -> None:
	global _typed, _last_ms
	now = pygame.time.get_ticks()
	if _last_ms is None:
		_last_ms = now
	dt = now - _last_ms
	_last_ms = now
	_typed = min(_typed + dt * setting.typing_speed / 1000.0, len(text))


def _start_typing_sound() -> None:
	global _sound_on
	if _audio_ok and not _sound_on:
		pygame.mixer.music.set_volume(setting.music_volume)
		pygame.mixer.music.play(-1, start=SOUND_START)
		_sound_on = True


def _stop_typing_sound() -> None:
	global _sound_on
	if _audio_ok and _sound_on:
		pygame.mixer.music.stop()
		_sound_on = False


def _get_cg(name: str) -> pygame.Surface:
	if name not in _cg_cache:
		for ext in ("png", "jpg", "jpeg"):
			path = f"./src/img/cg/{name}.{ext}"
			if os.path.exists(path):
				_cg_cache[name] = pygame.transform.scale(pygame.image.load(path), (WIDTH, HEIGHT))
				break
		else:
			raise FileNotFoundError(f"story CG not found: src/img/cg/{name}.*")
	return _cg_cache[name]


def _wrap(text: str, max_w: int) -> list[str]:
	lines: list[str] = []
	for paragraph in text.split("\n"):
		line = ""
		for ch in paragraph:
			if _font.size(line + ch)[0] > max_w:
				lines.append(line)
				line = ch
			else:
				line += ch
		lines.append(line)
	return lines


def _draw_textbox(screen: pygame.Surface, text: str, done: bool) -> None:
	box = pygame.Surface((WIDTH, BOX_H), pygame.SRCALPHA)
	box.fill((20, 20, 20, 180))
	screen.blit(box, (0, HEIGHT - BOX_H))

	y = HEIGHT - BOX_H + PAD
	for line in _wrap(text, WIDTH - PAD * 2):
		screen.blit(_font.render(line, True, (245, 245, 245)), (PAD, y))
		y += _font.get_linesize() + 6

	hint = _hint_font.render("點擊 / 空白鍵 繼續" if done else "點擊 跳過", True, (210, 210, 210))
	hint_rect = hint.get_rect(bottomright=(WIDTH - PAD, HEIGHT - 16))
	screen.blit(hint, hint_rect)
	if done:
		tx, cy = hint_rect.left - 18, hint_rect.centery
		pygame.draw.polygon(screen, (210, 210, 210), [(tx, cy - 6), (tx, cy + 6), (tx + 10, cy)])


def draw(screen: pygame.Surface) -> None:
	_ensure_init()
	if not _beats:
		return
	beat = _beats[_index]
	_update_typing(beat["text"])
	shown = int(_typed)
	done = shown >= len(beat["text"])
	if done:
		_stop_typing_sound()
	else:
		_start_typing_sound()
	screen.blit(_get_cg(beat["cg"]), (0, 0))
	_draw_textbox(screen, beat["text"][:shown], done)


def skip() -> None:
	global _index
	_stop_typing_sound()
	_index = len(_beats)


def advance() -> bool:
	global _index, _typed
	if not _beats:
		return True
	if _typed < len(_beats[_index]["text"]):
		_typed = float(len(_beats[_index]["text"]))
		_stop_typing_sound()
		return False
	_index += 1
	if _index >= len(_beats):
		_stop_typing_sound()
		return True
	_reset_typing()
	return False
