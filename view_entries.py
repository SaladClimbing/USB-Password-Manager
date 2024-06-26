from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS

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
	
    
    def get_username_at_position(position):
        return database.get_username(position)

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
    
    def clicked(self, keyboard, layout: KeyboardLayoutUS, website_names, database, position):
        username = database.get_username(website_names[position])
        password = database.get_password(website_names[position], username)
    
        layout.write(username)
        keyboard.send(Keycode.TAB)
        layout.write(password)
        keyboard.send(Keycode.ENTER)
    
    def render(self, position, database, website_names):
        username_at_position = get_username_at_position(position)
        username_ahead_position = get_username_at_position(position + 1)
        username_behind_position = get_username_at_position(position - 1)
        
        if position == 0:
            users = list(database.data[website_names[position]].keys())[0]
            self.update_label(
                0,
                website_names[position] + " ({})".format(username_at_position),
                website_names[position + 1] + " ({})".format(username_ahead_position),
                website_names[position + 2] + " ({})".format(get_username_at_position(position + 2)))
            
        elif position == len(website_names) - 1:
            self.update_label(
                2,
                website_names[position - 2] + " ({})".format(get_username_at_position(position - 2)),
                website_names[position - 1] + " ({})".format(username_behind_position),
                website_names[position] + " ({})".format(username_at_position))
            
        else:
            self.update_label(
                1,
                website_names[position - 1] + " ({})".format(username_behind_position),
                website_names[position] + " ({})".format(username_at_position),
                website_names[position + 1] + " ({})".format(username_ahead_position)
