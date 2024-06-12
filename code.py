import board
import usb_hid

from menu import MainMenu
from view_entries import ViewEntries
from state_manager import State_Manager, MENU_STATES

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
website_names = list(database.data.keys())

main_menu = MainMenu(display)
view_entries = ViewEntries(display)
rotary_encoder = Encoder()

position = None
last_position = None

state_manager = State_Manager(main_menu, view_entries)

state = MENU_STATES.MAIN_MENU

def rotary_clicked():
    main_menu.selected_color = 0x00FF00
    if state_manager.is_state(MENU_STATES.VIEW_ENTRIES):
        view_entries.clicked(keybaord, layout, website_names, database, position)
    if state_manager.is_state(MENU_STATES.MAIN_MENU):
        if relative_position == 0:
            state_manager.state = MENU_STATES.VIEW_ENTRIES
        elif relative_position == 1:
            state_manager.state = MENU_STATES.NEW_ENTRY
        elif relative_position == 2:
            state_manager.state = MENU_STATES.SETTINGS
        rotary_encoder.encoder.position = 0

# Main loop
while True:
    position = rotary_encoder.get_position()
    relative_position = position % NUMBER_OF_MENU_ITEMS
    
    state_manager.render()
    
    if position != last_position:
        last_position = position
        # rotary_encoder.encoder_changed(position)

    if not rotary_encoder.button.value and not rotary_encoder.encoder_button_held:
        rotary_encoder.encoder_button_held = True
        rotary_clicked()

    if rotary_encoder.button.value and rotary_encoder.encoder_button_held:
        rotary_encoder.encoder_button_held = False
        main_menu.selected_color = 0xFFFF00
        print("Button released")
