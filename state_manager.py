class MENU_STATES():
	MAIN_MENU    = 0,
	VIEW_ENTRIES = 1,
	NEW_ENTRY    = 2,
	SETTINGS     = 3

class State_Manager():
    def __init__(self, Main_Menu, View_Entries, Settings = NONE, state = MENU_STATES.MAIN_MENU):
        self.state = state
        self.Main_Menu = Main_Menu
        self.View_Entries = View_Entries
        self.Settings = Settings
    
    def render(self):
        if self.state == MENU_STATES.MAIN_MENU:
            main_menu.update_label(relative_position)
        
        if self.state == MENU_STATES.VIEW_ENTRIES:
            # Loops back around
            if position > len(website_names) - 1:
                rotary_encoder.encoder.position = 0
                position = rotary_encoder.get_position()
            elif position < 0: # Returns to the main menu when you go up at the top
               self.state = MENU_STATES.MAIN_MENU
            
            view_entries.render(position, database, website_names)
    
    def is_state(self, comparison_state):
        return comparison_state == self.state

    @property
    def state(self):
        return self.state
    
    @state.setter
    def state(self, new_state):
        self.state = new_state

    def __int__(self):
        return self.state
