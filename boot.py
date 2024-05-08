# SPDX-FileCopyrightText: 2017 Limor Fried for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""CircuitPython Essentials Storage logging boot.py file"""
import board
import digitalio
import storage # type: ignore

# For Gemma M0, Trinket M0, Metro M0/M4 Express, ItsyBitsy M0/M4 Express
switch = digitalio.DigitalInOut(board.D1)
switch.direction = digitalio.Direction.INPUT
switch.pull = digitalio.Pull.DOWN

if switch.value:
	print("Switch is pressed. CircuitPython write access to the drive is disabled.")
if not switch.value:
	print("Switch is not pressed. Enabling CircuitPython write access to the drive.")

# If the switch pin is connected to ground CircuitPython can write to the drive
storage.remount("/", readonly=switch.value)
# storage.disable_usb_drive()
