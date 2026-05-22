class hotkey_t:
	def __init__(self, keys: list[int]):
		self.keys = keys
		self.press = False
	def check_down(self, key: int):
		if key in self.keys:
			self.press = True
		return self
	def check_up(self, key: int):
		if key in self.keys:
			self.press = False
		return self
	def pressed(self) -> bool:
		return self.press
	