import os
import pygame
import bgm
import setting
import source

WIDTH, HEIGHT = 960, 720
FONT_PATH = os.path.join(os.path.dirname(__file__), "src", "fonts", "NotoSansTC.ttf")
BUTTON_DIR = os.path.join(os.path.dirname(__file__), "src", "img", "button")
CG_DIR = os.path.join(os.path.dirname(__file__), "src", "img", "cg")
CLICK_SOUND = os.path.join(os.path.dirname(__file__), "src", "audio", "button.mp3")
BTN_SCALE = 0.62

PANEL_FILL = (250, 250, 246, 168)
TEXT_MAIN = (34, 38, 44)
TEXT_SUB = (70, 76, 84)
TEXT_NOTE = (96, 102, 110)
TRACK_COLOR = (120, 126, 132)
HANDLE_COLOR = (44, 50, 60)
FIELD_FILL = (255, 255, 255)
FIELD_BORDER = (130, 136, 144)
FIELD_BORDER_ACTIVE = (52, 108, 170)
MESSAGE_COLOR = (185, 45, 45)


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
		self.key_prevent = KeyCapture()
		self.message = ""
		self._font = _cjk_font(28)
		self._hint = _cjk_font(20)
		self._note = _cjk_font(16)
		self._sliders = {"sfx": self.sfx, "music": self.music, "view": self.view, "typing": self.typing}
		self._bg = pygame.transform.smoothscale(
			pygame.image.load(os.path.join(CG_DIR, "back.png")).convert(), (WIDTH, HEIGHT))
		back = self._place_button("back", bottomright=(PANEL.right - 28, PANEL.bottom - 14))
		save = self._place_button("save", bottomright=(back["rect"].left - 22, PANEL.bottom - 14))
		self._buttons = {"save": save, "back": back}
		self._snapshot = setting.to_dict()
		self._click_sound = None
		self._click_loaded = False

	def _ensure_click(self):
		if self._click_loaded:
			return
		self._click_loaded = True
		if not pygame.mixer.get_init():
			try:
				pygame.mixer.init()
			except pygame.error as e:
				print(f"settings_page: 音訊初始化失敗：{e}")
				return
		try:
			self._click_sound = pygame.mixer.Sound(CLICK_SOUND)
			setting.register_sfx(self._click_sound)
		except pygame.error as e:
			print(f"settings_page: 載入 {CLICK_SOUND} 失敗：{e}")

	def _play_click(self):
		self._ensure_click()
		if self._click_sound is not None:
			self._click_sound.play()

	def _place_button(self, name, **anchor):
		img = pygame.image.load(os.path.join(BUTTON_DIR, f"{name}.png")).convert_alpha()
		img = pygame.transform.smoothscale(img, (round(img.get_width() * BTN_SCALE), round(img.get_height() * BTN_SCALE)))
		vis = img.get_bounding_rect()
		rect = vis.copy()
		for edge, value in anchor.items():
			setattr(rect, edge, value)
		return {"img": img, "pos": (rect.x - vis.x, rect.y - vis.y), "rect": rect}

	def _sync_from_setting(self):
		self.sfx.value = self.sfx._quantize(setting.sfx_volume)
		self.music.value = self.music._quantize(setting.music_volume)
		self.view.value = self.view._quantize(setting.tile_size)
		self.typing.value = self.typing._quantize(setting.typing_speed)
		self.seed.value = setting.configured_seed

	def enter(self):
		self._snapshot = setting.to_dict()
		self._sync_from_setting()
		self._defocus()
		self.message = ""

	def revert(self):
		setting.restore(self._snapshot)
		bgm.apply_volume()
		source.rescale()
		self._sync_from_setting()

	def _row_y(self, index):
		return FIRST_Y + index * ROW_H

	def slider_track(self, name):
		index = SLIDER_ORDER.index(name)
		return TRACK_X, self._row_y(index) + 12, TRACK_W

	def _seed_rect(self):
		return pygame.Rect(TRACK_X, self._row_y(4), TRACK_W, 32)

	def _key_rect(self, index):
		return pygame.Rect(TRACK_X, self._row_y(6 + index), 160, 32)

	def back_center(self):
		return self._buttons["back"]["rect"].center

	def save_center(self):
		return self._buttons["save"]["rect"].center

	def _apply(self):
		setting.sfx_volume = self.sfx.value
		setting.music_volume = self.music.value
		setting.typing_speed = int(self.typing.value)
		setting.configured_seed = self.seed.value
		setting.apply_audio()
		bgm.apply_volume()
		new_tile = int(self.view.value)
		if new_tile != setting.tile_size:
			setting.tile_size = new_tile
			source.rescale()

	def _conflict(self, key, which):
		keys = {
			"inv": setting.key_inventory,
			"set": setting.key_settings,
			"prevent": setting.key_prevent,
		}
		return any(name != which and key == value for name, value in keys.items())

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
				and not self.key_set.capturing and not self.key_prevent.capturing and not self.seed.focused:
				return "back"
			self._on_key_down(event)
		return None

	def _defocus(self):
		self.seed.focused = False
		self.key_inv.capturing = False
		self.key_set.capturing = False
		self.key_prevent.capturing = False

	def _on_mouse_down(self, pos):
		for action in ("save", "back"):
			if self._buttons[action]["rect"].collidepoint(pos):
				self._play_click()
				return action
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
		if self._key_rect(2).collidepoint(pos):
			self._defocus()
			self.key_prevent.start()
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
		if self.key_prevent.capturing:
			key = self.key_prevent.take(event)
			if key is not None:
				if self._conflict(key, "prevent"):
					self.message = "此鍵已被使用"
				else:
					setting.key_prevent = key
					self.message = ""
			return
		if self.seed.focused and self.seed.handle_key(event):
			self._apply()

	def draw(self, screen):
		screen.blit(self._bg, (0, 0))
		panel = pygame.Surface((PANEL.width, PANEL.height), pygame.SRCALPHA)
		pygame.draw.rect(panel, PANEL_FILL, panel.get_rect(), border_radius=18)
		screen.blit(panel, PANEL.topleft)

		title = self._font.render("SETTINGS", True, TEXT_MAIN)
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
			screen.blit(self._font.render(labels[name], True, TEXT_MAIN), (LABEL_X, y))
			tx, cy, tw = self.slider_track(name)
			pygame.draw.line(screen, TRACK_COLOR, (tx, cy), (tx + tw, cy), 4)
			frac = (s.value - s.vmin) / (s.vmax - s.vmin) if s.vmax != s.vmin else 0
			hx = int(tx + frac * tw)
			pygame.draw.circle(screen, HANDLE_COLOR, (hx, cy), 8)
			screen.blit(self._hint.render(fmt[name](s.value), True, TEXT_SUB), (tx + tw + 16, y))

		sy = self._row_y(4)
		screen.blit(self._font.render("種子碼", True, TEXT_MAIN), (LABEL_X, sy))
		sr = self._seed_rect()
		pygame.draw.rect(screen, FIELD_FILL, sr)
		pygame.draw.rect(screen, FIELD_BORDER_ACTIVE if self.seed.focused else FIELD_BORDER, sr, 2)
		seed_surf = self._hint.render(self.seed.value, True, TEXT_MAIN)
		screen.set_clip(sr.inflate(-6, -4))
		seed_x = sr.x + 6
		if seed_surf.get_width() > sr.width - 12:
			seed_x = sr.right - 6 - seed_surf.get_width()
		screen.blit(seed_surf, (seed_x, sr.y + 6))
		screen.set_clip(None)
		screen.blit(self._note.render("(下次開新遊戲生效)", True, TEXT_NOTE), (sr.x, sr.bottom + 2))

		ky = self._row_y(5)
		screen.blit(self._font.render("── 鍵盤設定 ──", True, TEXT_SUB), (LABEL_X, ky))
		for index, (label, key, cap) in enumerate([
			("開啟背包", setting.key_inventory, self.key_inv),
			("開設定頁", setting.key_settings, self.key_set),
			("蹲下", setting.key_prevent, self.key_prevent),
		]):
			y = self._row_y(6 + index)
			screen.blit(self._font.render(label, True, TEXT_MAIN), (LABEL_X, y))
			kr = self._key_rect(index)
			pygame.draw.rect(screen, FIELD_FILL, kr)
			pygame.draw.rect(screen, FIELD_BORDER_ACTIVE if cap.capturing else FIELD_BORDER, kr, 2)
			text = "請按鍵…" if cap.capturing else pygame.key.name(key)
			screen.blit(self._hint.render(text, True, TEXT_MAIN), (kr.x + 6, kr.y + 6))

		if self.message:
			screen.blit(self._hint.render(self.message, True, MESSAGE_COLOR), (LABEL_X, self._row_y(9)))
		for action in ("save", "back"):
			self._draw_button(screen, self._buttons[action])

	def _draw_button(self, screen, btn):
		img, pos, rect = btn["img"], btn["pos"], btn["rect"]
		if rect.collidepoint(pygame.mouse.get_pos()):
			big = pygame.transform.smoothscale(img, (round(img.get_width() * 1.08), round(img.get_height() * 1.08)))
			screen.blit(big, big.get_rect(center=img.get_rect(topleft=pos).center))
		else:
			screen.blit(img, pos)
