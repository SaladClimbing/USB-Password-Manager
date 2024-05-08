import board
import terminalio

from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font
from adafruit_seesaw import seesaw, rotaryio, digitalio

display = board.DISPLAY

text = "Hello, CircuitPython!"
font = bitmap_font.load_font("/fonts/35-Adobe-Helvetica-Bold.bdf")
color = 0xFFFFFF

# i2c = board.I2C()  # uses board.SCL and board.SDA
i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
seesaw = seesaw.Seesaw(i2c, addr=0x36)

seesaw_product = (seesaw.get_version() >> 16) & 0xFFFF
print("Found product {}".format(seesaw_product))
if seesaw_product != 4991:
    print("Wrong firmware loaded?  Expected 4991")

# Configure seesaw pin used to read knob button presses
# The internal pull up is enabled to prevent floating input
seesaw.pin_mode(24, seesaw.INPUT_PULLUP)
button = digitalio.DigitalIO(seesaw, 24)

encoder_button_held = False

encoder = rotaryio.IncrementalEncoder(seesaw)
last_position = None

ENCODER_UPPER_BOUND = 0xFFFFFF
ENCODER_LOWER_BOUND = 0x000000
ENCODER_RESET = 0

def encoder_changed():
    if (position > ENCODER_UPPER_BOUND) or (position < ENCODER_LOWER_BOUND):
        encoder.position = ENCODER_RESET
    print("Position: {}".format(position))

# Main loop
while True:
    position = encoder.position

    text_area = label.Label(font, text=text, color=color)
    text_area.x = 10
    text_area.y = 22
    display.root_group = text_area

    if position != last_position:
        last_position = position
        color = position
        encoder_changed()    

    if not button.value and not encoder_button_held:
        encoder_button_held = True
        position *= 10
        print("Button pressed")

    if button.value and encoder_button_held:
        encoder_button_held = False
        print("Button released")