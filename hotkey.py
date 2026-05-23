from typing import Callable

class hotkey_t:
	def __init__(self, keys: list[int], *, on_down: Callable[[], None] = None, on_up: Callable[[], None] = None):
		self.keys = keys
		self.press = False
		self.on_down = on_down
		self.on_up = on_up
	def check_down(self, key: int):
		if self.press == True:
			return self
		if key in self.keys:
			self.press = True
			if self.on_down != None:
				self.on_down()
		return self
	def check_up(self, key: int):
		if self.press == False:
			return self
		if key in self.keys:
			self.press = False
			if self.on_up != None:
				self.on_up()
		return self
	def pressed(self) -> bool:
		return self.press
