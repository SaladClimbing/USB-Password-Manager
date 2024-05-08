import board
from adafruit_seesaw import seesaw, rotaryio, digitalio # type: ignore

class Encoder:
    def __init__(self) -> None:
        i2c = board.STEMMA_I2C()
        self.seesaw = seesaw.Seesaw(i2c, addr=0x36)

        # Checks to make sure the rotary encoder is connected
        # If you're not using the Adafruit Rotary Encoder, you may need to comment this out
        seesaw_product = (self.seesaw.get_version() >> 16) & 0xFFFF
        print("Found product {}".format(seesaw_product))
        if seesaw_product != 4991:
            print("Wrong firmware loaded?  Expected 4991")
        
        # Configure seesaw pin used to read knob button presses
        # The internal pull up is enabled to prevent floating input
        self.seesaw.pin_mode(24, self.seesaw.INPUT_PULLUP)
        self.button = digitalio.DigitalIO(self.seesaw, 24)

        self.encoder_button_held = False

        self.encoder = rotaryio.IncrementalEncoder(self.seesaw)

        self.ENCODER_UPPER_BOUND = 2
        self.ENCODER_LOWER_BOUND = 0
        self.ENCODER_RESET = 0



    def encoder_changed(self, position: int) -> None:
        if position > self.ENCODER_UPPER_BOUND:
            self.encoder.position = self.ENCODER_LOWER_BOUND
        if position < self.ENCODER_LOWER_BOUND:
            self.encoder.position = self.ENCODER_UPPER_BOUND
    
    def get_position(self):
        return self.encoder.position