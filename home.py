import pygame

WIDTH, HEIGHT = 960, 720
BTN_SCALE = 1.5
BUTTON_SOUND = "./src/audio/button.mp3"

_cover: pygame.Surface = None
_font: pygame.font.Font = None
_buttons: dict[str, dict] = {}
_back_button: dict = None
_click_sound: pygame.mixer.Sound | None = None


def _place(name: str, **anchor) -> dict:
	img = pygame.image.load(f"./src/img/button/{name}.png").convert_alpha()
	img = pygame.transform.smoothscale(img, (round(img.get_width() * BTN_SCALE), round(img.get_height() * BTN_SCALE)))
	vis = img.get_bounding_rect()
	screen_rect = vis.copy()
	for edge, value in anchor.items():
		setattr(screen_rect, edge, value)
	pos = (screen_rect.x - vis.x, screen_rect.y - vis.y)
	return {"img": img, "pos": pos, "rect": screen_rect}


def _ensure_init():
	global _cover, _font, _buttons, _back_button, _click_sound
	if _cover is not None:
		return
	_cover = pygame.transform.scale(pygame.image.load("./src/img/cg/home_page.png"), (WIDTH, HEIGHT))
	_font = pygame.font.SysFont(None, 40)

	right_margin, bottom_margin, gap = 95, 60, 34
	setting = _place("setting", bottomright=(WIDTH - right_margin, HEIGHT - bottom_margin))
	start = _place("start", bottomright=(WIDTH - right_margin, setting["rect"].top - gap))
	_buttons = {"start": start, "settings": setting}
	_back_button = _place("back", topleft=(40, 40))

	if not pygame.mixer.get_init():
		try:
			pygame.mixer.init()
		except pygame.error as e:
			print(f"home: 音訊初始化失敗，按鈕將無音效：{e}")
	if pygame.mixer.get_init():
		try:
			_click_sound = pygame.mixer.Sound(BUTTON_SOUND)
		except pygame.error as e:
			print(f"home: 載入 {BUTTON_SOUND} 失敗，按鈕將無音效：{e}")


def _play_click() -> None:
	if _click_sound is not None:
		_click_sound.play()


def _draw_button(screen: pygame.Surface, btn: dict) -> None:
	img, pos, rect = btn["img"], btn["pos"], btn["rect"]
	if rect.collidepoint(pygame.mouse.get_pos()):
		big = pygame.transform.smoothscale(img, (round(img.get_width() * 1.08), round(img.get_height() * 1.08)))
		screen.blit(big, big.get_rect(center=img.get_rect(topleft=pos).center))
	else:
		screen.blit(img, pos)


def draw(screen: pygame.Surface) -> None:
	_ensure_init()
	screen.blit(_cover, (0, 0))
	for btn in _buttons.values():
		_draw_button(screen, btn)


def handle_click(pos: tuple[int, int]) -> str | None:
	_ensure_init()
	for key, btn in _buttons.items():
		if btn["rect"].collidepoint(pos):
			_play_click()
			return key
	return None


def draw_settings(screen: pygame.Surface) -> None:
	_ensure_init()
	screen.fill((232, 240, 232))
	title = _font.render("SETTINGS", True, (70, 58, 48))
	screen.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
	_draw_button(screen, _back_button)


def handle_settings_click(pos: tuple[int, int]) -> str | None:
	_ensure_init()
	if _back_button["rect"].collidepoint(pos):
		_play_click()
		return "back"
	return None
