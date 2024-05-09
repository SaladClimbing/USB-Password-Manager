import displayio # type: ignore

from adafruit_display_text import label # type: ignore
from adafruit_bitmap_font import bitmap_font # type: ignore

class MainMenu:
	def __init__(self, display):
		self.font = bitmap_font.load_font("/fonts/35-Adobe-Helvetica-Bold.bdf")
		self.color = 0xFFFFFF
		self.selected_color = 0xFFFF00

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

class ViewEntries:
	def __init__(self, display):
		self.font = bitmap_font.load_font("/fonts/35-Adobe-Helvetica-Bold.bdf")
		self.color = 0xFFFFFF
		self.selected_color = 0xFFFF00

		# Text Labels
		self.text_position_X = 10
		self.text_position_Y = 22
		self.text_height = 35

		self.display = display

		self.update_all()
	
	def update_top_label(self, top, color):
		self.top_label = label.Label(self.font, text=top, color=color)
		self.top_label.x = self.text_position_X
		self.top_label.y = self.text_position_Y
	
	def update_middle_label(self, middle, color):
		self.middle_label = label.Label(self.font, text=middle, color=color)
		self.middle_label.x = self.text_position_X
		self.middle_label.y = self.text_position_Y + self.text_height

	def update_bottom_label(self, bottom, color):
		self.bottom_label = label.Label(self.font, text=bottom, color=color)
		self.bottom_label.x = self.text_position_X
		self.bottom_label.y = self.text_position_Y + self.text_height * 2

	def update_label(self, label_index, top="", middle="", bottom=""):
		self.update_all(top=top, middle=middle, bottom=bottom)
		if label_index == 0:
			self.update_top_label(top, self.selected_color)
		elif label_index == 1:
			self.update_middle_label(middle, self.selected_color)
		elif label_index == 2:
			self.update_bottom_label(bottom, self.selected_color)
		self.update_group()

	def update_all(self, top="", middle="", bottom="", color=0xFFFFFF):
		self.top_label = label.Label(self.font, text=top, color=color)
		self.top_label.x = self.text_position_X
		self.top_label.y = self.text_position_Y

		self.middle_label = label.Label(self.font, text=middle, color=color)
		self.middle_label.x = self.text_position_X
		self.middle_label.y = self.text_position_Y + self.text_height

		self.bottom_label = label.Label(self.font, text=bottom, color=color)
		self.bottom_label.x = self.text_position_X
		self.bottom_label.y = self.text_position_Y + self.text_height * 2

	def update_group(self):
		self.text_group = displayio.Group()
		self.text_group.insert(0, self.top_label)
		self.text_group.insert(1, self.middle_label)
		self.text_group.insert(2, self.bottom_label)
		self.display.root_group = self.text_group

class MenuStates():
	MAIN_MENU    = 0,
	VIEW_ENTRIES = 1,
	NEW_ENTRY    = 2,
	SETTINGS     = 3