import pygame

# Front-end menu scenes (cover / settings). The game loop lives in main.py.

WIDTH, HEIGHT = 960, 720

_cover: pygame.Surface = None
_font: pygame.font.Font = None
# button key -> (rect, label). Placeholder rectangles for now; swap in images later.
_buttons: dict[str, tuple[pygame.Rect, str]] = {}
_back_button: tuple[pygame.Rect, str] = None


def _ensure_init():
	# Lazy init: pygame must be initialised and the display created first,
	# so this can't run at import time (main.py imports home before pygame.init()).
	global _cover, _font, _buttons, _back_button
	if _cover is not None:
		return
	_cover = pygame.transform.scale(pygame.image.load("./cg/home_page.png"), (WIDTH, HEIGHT))
	_font = pygame.font.SysFont(None, 40)

	bw, bh, gap, margin = 200, 60, 18, 28
	x = WIDTH - margin - bw
	# stacked in the bottom-right corner
	_buttons = {
		"start": (pygame.Rect(x, HEIGHT - margin - bh * 2 - gap, bw, bh), "START"),
		"settings": (pygame.Rect(x, HEIGHT - margin - bh, bw, bh), "SETTING"),
	}
	_back_button = (pygame.Rect(margin, margin, 160, 56), "< BACK")


def _draw_button(screen: pygame.Surface, rect: pygame.Rect, label: str) -> None:
	hovered = rect.collidepoint(pygame.mouse.get_pos())
	fill = (255, 250, 240) if hovered else (240, 228, 210)
	pygame.draw.rect(screen, fill, rect, border_radius=12)
	pygame.draw.rect(screen, (90, 78, 66), rect, width=3, border_radius=12)
	text = _font.render(label, True, (70, 58, 48))
	screen.blit(text, text.get_rect(center=rect.center))


def draw(screen: pygame.Surface) -> None:
	_ensure_init()
	screen.blit(_cover, (0, 0))
	for rect, label in _buttons.values():
		_draw_button(screen, rect, label)


def handle_click(pos: tuple[int, int]) -> str | None:
	"""Return the clicked button key ('start' / 'settings'), or None."""
	_ensure_init()
	for key, (rect, _label) in _buttons.items():
		if rect.collidepoint(pos):
			return key
	return None


def draw_settings(screen: pygame.Surface) -> None:
	_ensure_init()
	screen.fill((232, 240, 232))
	title = _font.render("SETTINGS", True, (70, 58, 48))
	screen.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
	_draw_button(screen, _back_button[0], _back_button[1])


def handle_settings_click(pos: tuple[int, int]) -> str | None:
	"""Return 'back' if the back button was clicked, else None."""
	_ensure_init()
	if _back_button[0].collidepoint(pos):
		return "back"
	return None
