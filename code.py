import board
import usb_hid

from menu import MainMenu, MenuStates
from view_entries import ViewEntries

from encoder import Encoder

from database import PasswordDatabase

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

display = board.DISPLAY

NUMBER_OF_MENU_ITEMS = 3

database = PasswordDatabase("/passwords.json")
keyboard = Keyboard(usb_hid.devices) # Initialize Keyboard
layout = KeyboardLayoutUS(keyboard) # Set Keyboard Layout
web_keys = list(database.data.keys())

main_menu = MainMenu(display)
view_entries = ViewEntries(display)
rotary_encoder = Encoder()

last_position = None
position = None
state = MenuStates.MAIN_MENU

# Main loop
while True:
    position = rotary_encoder.get_position()
    position_mod = position % NUMBER_OF_MENU_ITEMS
    
    if state == MenuStates.MAIN_MENU:
        main_menu.update_label(position_mod)

    if state == MenuStates.VIEW_ENTRIES:
        if position > len(web_keys) - 1:
            rotary_encoder.encoder.position = 0
            position = rotary_encoder.get_position()
        elif position < 0:
            state = MenuStates.MAIN_MENU
        view_entries.render(position, database, web_keys)
    
    if position != last_position:
        last_position = position
        # rotary_encoder.encoder_changed(position)

    if not rotary_encoder.button.value and not rotary_encoder.encoder_button_held:
        rotary_encoder.encoder_button_held = True
        main_menu.selected_color = 0x00FF00
        if state == MenuStates.VIEW_ENTRIES:
            view_entries.clicked(keyboard, layout, web_keys, database, position)
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
