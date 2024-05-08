import displayio # type: ignore

from adafruit_display_text import label # type: ignore
from adafruit_bitmap_font import bitmap_font # type: ignore

class MainMenu:
	def __init__(self, display):
		text = "Hello, CircuitPython!"
		font = bitmap_font.load_font("/fonts/35-Adobe-Helvetica-Bold.bdf")
		color = 0xFFFFFF

		# Text Labels
		self.view_entries = label.Label(font, text="View Entries", color=color)
		self.view_entries.x = 10
		self.view_entries.y = 22

		self.new_entry = label.Label(font, text="New Entry", color=color)
		self.new_entry.x = 10
		self.new_entry.y = 57

		self.text_group = displayio.Group()
		self.text_group.append(self.view_entries)
		self.text_group.append(self.new_entry)
		
		self.display = display
		self.display.root_group = self.text_group