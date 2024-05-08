import board
from adafruit_seesaw import seesaw, rotaryio, digitalio

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

ENCODER_UPPER_BOUND = 10
ENCODER_LOWER_BOUND = 0
ENCODER_RESET = 0

def encoder_changed():
    if (position > ENCODER_UPPER_BOUND) or (position < ENCODER_LOWER_BOUND):
        encoder.position = ENCODER_RESET
    print("Position: {}".format(position))

# Main loop
while True:
    position = encoder.position

    if position != last_position:
        last_position = position
        encoder_changed()    

    if not button.value and not encoder_button_held:
        encoder_button_held = True
        print("Button pressed")

    if button.value and encoder_button_held:
        encoder_button_held = False
        print("Button released")
