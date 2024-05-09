import board
import digitalio
from menu import MainMenu, ViewEntries, MenuStates
from encoder import Encoder
from database import PasswordDatabase
display = board.DISPLAY

db = PasswordDatabase("/passwords.json")
keys = list(db.data.keys())

main_menu = MainMenu(display)
view_entries = ViewEntries(display)
rotary_encoder = Encoder()

last_position = None
position = None
state = MenuStates.MAIN_MENU

# Main loop
while True:
    position = rotary_encoder.get_position()
    position_mod = position % 3
    
    if state == MenuStates.MAIN_MENU:
        main_menu.update_label(position_mod)

    if state == MenuStates.VIEW_ENTRIES:
        if position == 0:
            users = list(db.data[keys[position]].keys())[0]
            view_entries.update_label(
                0,
                keys[position] + " ({})".format(list(db.data[keys[position]].keys())[0]),
                keys[position + 1] + " ({})".format(list(db.data[keys[position + 1]].keys())[0]),
                keys[position + 2] + " ({})".format(list(db.data[keys[position + 2]].keys())[0]))
            
        elif position == len(keys) - 1:
            view_entries.update_label(
                2,
                keys[position - 2] + " ({})".format(list(db.data[keys[position - 2]].keys())[0]),
                keys[position - 1] + " ({})".format(list(db.data[keys[position - 1]].keys())[0]),
                keys[position] + " ({})".format(list(db.data[keys[position]].keys())[0]))
            
        else:
            view_entries.update_label(
                1,
                keys[position - 1] + " ({})".format(list(db.data[keys[position - 1]].keys())[0]),
                keys[position] + " ({})".format(list(db.data[keys[position]].keys())[0]),
                keys[position + 1] + " ({})".format(list(db.data[keys[position + 1]].keys())[0]))

    if position != last_position:
        last_position = position
        # rotary_encoder.encoder_changed(position)

    if not rotary_encoder.button.value and not rotary_encoder.encoder_button_held:
        rotary_encoder.encoder_button_held = True
        main_menu.selected_color = 0x00FF00
        if state == MenuStates.MAIN_MENU:
            if position == 0:
                state = MenuStates.VIEW_ENTRIES
            elif position == 1:
                state = MenuStates.NEW_ENTRY
            elif position == 2:
                state = MenuStates.SETTINGS
        print("Button pressed")

    if rotary_encoder.button.value and rotary_encoder.encoder_button_held:
        rotary_encoder.encoder_button_held = False
        main_menu.selected_color = 0xFF0000
        print("Button released")
    