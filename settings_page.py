import os
import pygame
import setting
import source

WIDTH, HEIGHT = 960, 720
FONT_PATH = os.path.join(os.path.dirname(__file__), "src", "fonts", "NotoSansTC.ttf")


def _cjk_font(size: int) -> pygame.font.Font:
	if os.path.exists(FONT_PATH):
		return pygame.font.Font(FONT_PATH, size)
	return pygame.font.SysFont(None, size)


class Slider:
	def __init__(self, vmin, vmax, value, step=1):
		self.vmin = vmin
		self.vmax = vmax
		self.step = step
		self.dragging = False
		self.value = self._quantize(value)

	def _quantize(self, v):
		v = max(self.vmin, min(self.vmax, v))
		steps = round((v - self.vmin) / self.step)
		return round(self.vmin + steps * self.step, 10)

	def set_from_x(self, mouse_x, track_x, track_w):
		frac = (mouse_x - track_x) / track_w if track_w else 0
		frac = max(0.0, min(1.0, frac))
		self.value = self._quantize(self.vmin + frac * (self.vmax - self.vmin))
		return self.value


class TextInput:
	def __init__(self, value="", max_len=24):
		self.value = value
		self.max_len = max_len
		self.focused = False

	def handle_key(self, event):
		if not self.focused:
			return False
		if event.key == pygame.K_BACKSPACE:
			if self.value:
				self.value = self.value[:-1]
				return True
			return False
		ch = event.unicode
		if ch and ch.isprintable() and len(self.value) < self.max_len:
			self.value += ch
			return True
		return False


class KeyCapture:
	def __init__(self):
		self.capturing = False

	def start(self):
		self.capturing = True

	def take(self, event):
		if not self.capturing:
			return None
		self.capturing = False
		return event.key


PANEL = pygame.Rect(150, 60, 660, 600)
LABEL_X = 190
TRACK_X = 430
TRACK_W = 250
ROW_H = 56
FIRST_Y = 140
SLIDER_ORDER = ["sfx", "music", "view", "typing"]


class SettingsPage:
	def __init__(self):
		self.sfx = Slider(0.0, 1.0, setting.sfx_volume, step=0.05)
		self.music = Slider(0.0, 1.0, setting.music_volume, step=0.05)
		self.view = Slider(34, 72, setting.tile_size, step=2)
		self.typing = Slider(5, 60, setting.typing_speed, step=1)
		self.seed = TextInput(setting.configured_seed, max_len=24)
		self.key_inv = KeyCapture()
		self.key_set = KeyCapture()
		self.message = ""
		self._font = _cjk_font(28)
		self._hint = _cjk_font(20)
		self._note = _cjk_font(16)
		self._sliders = {"sfx": self.sfx, "music": self.music, "view": self.view, "typing": self.typing}

	def _row_y(self, index):
		return FIRST_Y + index * ROW_H

	def slider_track(self, name):
		index = SLIDER_ORDER.index(name)
		return TRACK_X, self._row_y(index) + 12, TRACK_W

	def _seed_rect(self):
		return pygame.Rect(TRACK_X, self._row_y(4), TRACK_W, 32)

	def _key_rect(self, index):
		return pygame.Rect(TRACK_X, self._row_y(6 + index), 160, 32)

	def _back_rect(self):
		return pygame.Rect(PANEL.right - 140, PANEL.bottom - 56, 110, 40)

	def back_center(self):
		r = self._back_rect()
		return r.centerx, r.centery

	def _apply(self):
		setting.sfx_volume = self.sfx.value
		setting.music_volume = self.music.value
		setting.typing_speed = int(self.typing.value)
		setting.configured_seed = self.seed.value
		setting.apply_audio()
		new_tile = int(self.view.value)
		if new_tile != setting.tile_size:
			setting.tile_size = new_tile
			source.rescale()

	def _conflict(self, key, which):
		other = setting.key_settings if which == "inv" else setting.key_inventory
		return key == other

	def handle_event(self, event):
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
			return self._on_mouse_down(event.pos)
		if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
			for s in self._sliders.values():
				s.dragging = False
		if event.type == pygame.MOUSEMOTION:
			for name, s in self._sliders.items():
				if s.dragging:
					tx, _, tw = self.slider_track(name)
					s.set_from_x(event.pos[0], tx, tw)
					self._apply()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE and not self.key_inv.capturing \
				and not self.key_set.capturing and not self.seed.focused:
				return "back"
			self._on_key_down(event)
		return None

	def _defocus(self):
		self.seed.focused = False
		self.key_inv.capturing = False
		self.key_set.capturing = False

	def _on_mouse_down(self, pos):
		if self._back_rect().collidepoint(pos):
			return "back"
		for name, s in self._sliders.items():
			tx, cy, tw = self.slider_track(name)
			track = pygame.Rect(tx, cy - 12, tw + 1, 24)
			if track.collidepoint(pos):
				self._defocus()
				s.dragging = True
				s.set_from_x(pos[0], tx, tw)
				self._apply()
				return None
		if self._seed_rect().collidepoint(pos):
			self._defocus()
			self.seed.focused = True
			return None
		if self._key_rect(0).collidepoint(pos):
			self._defocus()
			self.key_inv.start()
			return None
		if self._key_rect(1).collidepoint(pos):
			self._defocus()
			self.key_set.start()
			return None
		self._defocus()
		return None

	def _on_key_down(self, event):
		if self.key_inv.capturing:
			key = self.key_inv.take(event)
			if key is not None:
				if self._conflict(key, "inv"):
					self.message = "此鍵已被使用"
				else:
					setting.key_inventory = key
					self.message = ""
			return
		if self.key_set.capturing:
			key = self.key_set.take(event)
			if key is not None:
				if self._conflict(key, "set"):
					self.message = "此鍵已被使用"
				else:
					setting.key_settings = key
					self.message = ""
			return
		if self.seed.focused and self.seed.handle_key(event):
			self._apply()

	def draw(self, screen):
		panel = pygame.Surface((PANEL.width, PANEL.height), pygame.SRCALPHA)
		panel.fill((20, 24, 32, 200))
		screen.blit(panel, PANEL.topleft)

		title = self._font.render("SETTINGS", True, (245, 245, 245))
		screen.blit(title, title.get_rect(midtop=(PANEL.centerx, PANEL.top + 16)))

		labels = {"sfx": "音效大小", "music": "音樂大小", "view": "視野", "typing": "打字機速度"}
		fmt = {
			"sfx": lambda v: f"{int(v * 100)}%",
			"music": lambda v: f"{int(v * 100)}%",
			"view": lambda v: f"{v / 48:.1f}x",
			"typing": lambda v: f"{int(v)}",
		}
		for name in SLIDER_ORDER:
			index = SLIDER_ORDER.index(name)
			y = self._row_y(index)
			s = self._sliders[name]
			screen.blit(self._font.render(labels[name], True, (230, 230, 230)), (LABEL_X, y))
			tx, cy, tw = self.slider_track(name)
			pygame.draw.line(screen, (120, 120, 130), (tx, cy), (tx + tw, cy), 4)
			frac = (s.value - s.vmin) / (s.vmax - s.vmin) if s.vmax != s.vmin else 0
			hx = int(tx + frac * tw)
			pygame.draw.circle(screen, (235, 235, 245), (hx, cy), 8)
			screen.blit(self._hint.render(fmt[name](s.value), True, (210, 210, 210)), (tx + tw + 16, y))

		sy = self._row_y(4)
		screen.blit(self._font.render("種子碼", True, (230, 230, 230)), (LABEL_X, sy))
		sr = self._seed_rect()
		pygame.draw.rect(screen, (60, 64, 74), sr)
		pygame.draw.rect(screen, (235, 235, 245) if self.seed.focused else (120, 120, 130), sr, 2)
		seed_surf = self._hint.render(self.seed.value, True, (245, 245, 245))
		screen.set_clip(sr.inflate(-6, -4))
		seed_x = sr.x + 6
		if seed_surf.get_width() > sr.width - 12:
			seed_x = sr.right - 6 - seed_surf.get_width()
		screen.blit(seed_surf, (seed_x, sr.y + 6))
		screen.set_clip(None)
		screen.blit(self._note.render("(下次開新遊戲生效)", True, (170, 170, 180)), (sr.x, sr.bottom + 2))

		ky = self._row_y(5)
		screen.blit(self._font.render("── 鍵盤設定 ──", True, (200, 200, 210)), (LABEL_X, ky))
		for index, (label, key, cap) in enumerate([
			("開啟背包", setting.key_inventory, self.key_inv),
			("開設定頁", setting.key_settings, self.key_set),
		]):
			y = self._row_y(6 + index)
			screen.blit(self._font.render(label, True, (230, 230, 230)), (LABEL_X, y))
			kr = self._key_rect(index)
			pygame.draw.rect(screen, (60, 64, 74), kr)
			pygame.draw.rect(screen, (235, 235, 245) if cap.capturing else (120, 120, 130), kr, 2)
			text = "請按鍵…" if cap.capturing else pygame.key.name(key)
			screen.blit(self._hint.render(text, True, (245, 245, 245)), (kr.x + 6, kr.y + 6))

		if self.message:
			screen.blit(self._hint.render(self.message, True, (255, 180, 180)), (LABEL_X, self._row_y(8)))
		br = self._back_rect()
		pygame.draw.rect(screen, (70, 90, 70), br)
		pygame.draw.rect(screen, (200, 220, 200), br, 2)
		back = self._font.render("返回", True, (235, 245, 235))
		screen.blit(back, back.get_rect(center=br.center))
