import board
import digitalio
from menu import MainMenu
from encoder import Encoder
from database import PasswordDatabase
display = board.DISPLAY

main_menu = MainMenu(display)
rotary_encoder = Encoder()

last_position = None
position = None

d1 = digitalio.DigitalInOut(board.D1)
d1.direction = digitalio.Direction.INPUT
d1.pull = digitalio.Pull.DOWN

db = PasswordDatabase("/passwords.json")
db.add_password("Google", "user", "password")

# Main loop
while True:
    position = rotary_encoder.get_position()

    main_menu.update_label(position)

    if d1.value:
        main_menu.selected_color = 0x0000FF
    else:
        main_menu.selected_color = 0xFF0000

    if position != last_position:
        last_position = position
        rotary_encoder.encoder_changed(position)

    if not rotary_encoder.button.value and not rotary_encoder.encoder_button_held:
        rotary_encoder.encoder_button_held = True
        main_menu.selected_color = 0x00FF00
        print("Button pressed")

    if rotary_encoder.button.value and rotary_encoder.encoder_button_held:
        rotary_encoder.encoder_button_held = False
        main_menu.selected_color = 0xFF0000
        print("Button released")
