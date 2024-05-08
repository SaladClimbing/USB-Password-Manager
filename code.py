import board
from menu import MainMenu
from encoder import Encoder

display = board.DISPLAY

main_menu = MainMenu(display)
rotary_encoder = Encoder()

last_position = None
position = None

# Main loop
while True:
    position = rotary_encoder.get_position()

    main_menu.update_label(position)

    if position != last_position:
        last_position = position
        rotary_encoder.encoder_changed(position)

    if not rotary_encoder.button.value and not rotary_encoder.encoder_button_held:
        encoder_button_held = True
        print("Button pressed")

    if rotary_encoder.button.value and rotary_encoder.encoder_button_held:
        encoder_button_held = False
        print("Button released")
