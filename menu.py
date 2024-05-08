import displayio # type: ignore

from adafruit_display_text import label # type: ignore
from adafruit_bitmap_font import bitmap_font # type: ignore

class MainMenu:
	def __init__(self, display):
		text = "Hello, CircuitPython!"
		self.font = bitmap_font.load_font("/fonts/35-Adobe-Helvetica-Bold.bdf")
		self.color = 0xFFFFFF
		self.selected_color = 0xFF0000

		# Text Labels
		self.text_position_X = 10
		self.text_position_Y = 22
		self.text_height = 35

		self.update_view_entries(self.color)
		self.update_new_entry(self.color)
		self.update_settings(self.color)

		self.display = display

		self.update_group()
	
	def update_group(self):
		self.text_group = displayio.Group()
		self.text_group.insert(0, self.view_entries)
		self.text_group.insert(1, self.new_entry)
		self.text_group.insert(2, self.settings)

		self.display.root_group = self.text_group
	
	def update_view_entries(self, color):
		self.view_entries = label.Label(self.font, text="View Entries", color=color)
		self.view_entries.x = self.text_position_X
		self.view_entries.y = self.text_position_Y

	def update_new_entry(self, color):
		self.new_entry = label.Label(self.font, text="New Entry", color=color)
		self.new_entry.x = self.text_position_X
		self.new_entry.y = self.text_position_Y + self.text_height
	
	def update_settings(self, color):
		self.settings = label.Label(self.font, text="Settings", color=color)
		self.settings.x = self.text_position_X
		self.settings.y = self.text_position_Y + self.text_height * 2

	def update_all(self, color):
		self.update_view_entries(color)
		self.update_new_entry(color)
		self.update_settings(color)

	def update_label(self, label_index):
		self.update_all(0xFFFFFF)
		if label_index == 0:
			self.update_view_entries(self.selected_color)
		elif label_index == 1:
			self.update_new_entry(self.selected_color)
		elif label_index == 2:
			self.update_settings(self.selected_color)
		self.update_group()
