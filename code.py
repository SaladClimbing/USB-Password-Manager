import board
import usb_hid

from menu import MainMenu, ViewEntries, MenuStates
from encoder import Encoder
from database import PasswordDatabase
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

display = board.DISPLAY

db = PasswordDatabase("/passwords.json")
kbd = Keyboard(usb_hid.devices) # Initialize Keyboard
layout = KeyboardLayoutUS(kbd) # Set Keyboard Layout
web_keys = list(db.data.keys())

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
        if position > len(web_keys) - 1:
            rotary_encoder.encoder.position = 0
            position = rotary_encoder.get_position()
        elif position < 0:
            state = MenuStates.MAIN_MENU
        
        if position == 0:
            users = list(db.data[web_keys[position]].keys())[0]
            view_entries.update_label(
                0,
                web_keys[position] + " ({})".format(db.get_username(web_keys[position])),
                web_keys[position + 1] + " ({})".format(db.get_username(web_keys[position + 1])),
                web_keys[position + 2] + " ({})".format(db.get_username(web_keys[position + 2])))
            
        elif position == len(web_keys) - 1:
            view_entries.update_label(
                2,
                web_keys[position - 2] + " ({})".format(db.get_username(web_keys[position - 2])),
                web_keys[position - 1] + " ({})".format(db.get_username(web_keys[position - 1])),
                web_keys[position] + " ({})".format(db.get_username(web_keys[position])))
            
        else:
            view_entries.update_label(
                1,
                web_keys[position - 1] + " ({})".format(db.get_username(web_keys[position - 1])),
                web_keys[position] + " ({})".format(db.get_username(web_keys[position])),
                web_keys[position + 1] + " ({})".format(db.get_username(web_keys[position + 1])))

    if position != last_position:
        last_position = position
        # rotary_encoder.encoder_changed(position)

    if not rotary_encoder.button.value and not rotary_encoder.encoder_button_held:
        rotary_encoder.encoder_button_held = True
        main_menu.selected_color = 0x00FF00
        if state == MenuStates.VIEW_ENTRIES:
            layout.write(db.get_username(web_keys[position]))
            kbd.send(Keycode.TAB)
            layout.write(db.get_password(web_keys[position], db.get_username(web_keys[position])))
            kbd.send(Keycode.ENTER)
        if state == MenuStates.MAIN_MENU:
            if position_mod == 0:
                state = MenuStates.VIEW_ENTRIES
            elif position_mod == 1:
                state = MenuStates.NEW_ENTRY
            elif position_mod == 2:
                state = MenuStates.SETTINGS
            rotary_encoder.encoder.position = 0
        print("Button pressed")

    if rotary_encoder.button.value and rotary_encoder.encoder_button_held:
        rotary_encoder.encoder_button_held = False
        main_menu.selected_color = 0xFFFF00
        print("Button released")
