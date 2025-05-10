from digitalio import DigitalInOut, Direction, Pull
import board
import time
import os
import usb_hid
import json
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode


# HID devices
cc = ConsumerControl(usb_hid.devices)
keyboard = Keyboard(usb_hid.devices)
keyboard_layout = KeyboardLayoutUS(keyboard)

# Twój specjalny układ pinów
sw1 = board.GP0
sw2 = board.GP1
sw3 = board.GP2
sw4 = board.GP3
sw5 = board.GP4
sw6 = board.GP6
sw7 = board.GP7
sw8 = board.GP8
sw9 = board.GP9

btn1 = DigitalInOut(sw1)
btn1.direction = Direction.INPUT
btn1.pull = Pull.DOWN

btn2 = DigitalInOut(sw2)
btn2.direction = Direction.INPUT
btn2.pull = Pull.DOWN

btn3 = DigitalInOut(sw3)
btn3.direction = Direction.INPUT
btn3.pull = Pull.DOWN

btn4 = DigitalInOut(sw9)
btn4.direction = Direction.INPUT
btn4.pull = Pull.DOWN

btn5 = DigitalInOut(sw5)
btn5.direction = Direction.INPUT
btn5.pull = Pull.DOWN

btn6 = DigitalInOut(sw4)
btn6.direction = Direction.INPUT
btn6.pull = Pull.DOWN

btn7 = DigitalInOut(sw8)
btn7.direction = Direction.INPUT
btn7.pull = Pull.DOWN

btn8 = DigitalInOut(sw7)
btn8.direction = Direction.INPUT
btn8.pull = Pull.DOWN

btn9 = DigitalInOut(sw6)
btn9.direction = Direction.INPUT
btn9.pull = Pull.DOWN

buttons = [btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9]

shortcut_file= "shortcut_config.json"

if shortcut_file not in os.listdir("/"):
    raise RuntimeError("Brakuje pliku shortcut_config.json!")

with open(shortcut_file, "r") as f:
    shortcuts = json.load(f)

# Mapowanie nazw na kody
modifier_map = {
    "ctrl": Keycode.CONTROL,
    "shift": Keycode.SHIFT,
    "alt": Keycode.ALT,
    "win": Keycode.WINDOWS
}

key_map = {
    "a": Keycode.A, "b": Keycode.B, "c": Keycode.C, "v": Keycode.V, "z": Keycode.Z,
    "f1": Keycode.F1, "f2": Keycode.F2, "f3": Keycode.F3, "f4": Keycode.F4,
    "f5": Keycode.F5, "f6": Keycode.F6, "f7": Keycode.F7, "f8": Keycode.F8,
    "1": Keycode.ONE, "2": Keycode.TWO, "3": Keycode.THREE,
    "4": Keycode.FOUR, "5": Keycode.FIVE, "6": Keycode.SIX,
    "7": Keycode.SEVEN, "8": Keycode.EIGHT, "9": Keycode.NINE,
}

prev_states = [False] * 9

# ... reszta kodu powyżej bez zmian

while True:
    for i in range(9):
        btn = buttons[i]
        if btn.value and not prev_states[i]:
            shortcut = shortcuts[i].lower()

            if shortcut.startswith("open:"):
                url = shortcut[5:].strip()
                # Otwórz okno "Uruchom"
                keyboard.press(Keycode.WINDOWS, Keycode.R)
                keyboard.release_all()
                time.sleep(0.5)
                # Wpisz URL
                keyboard_layout.write(url)
                time.sleep(0.2)
                keyboard.press(Keycode.ENTER)
                keyboard.release_all()

            elif shortcut in ["volume up", "volume_up"]:
                cc.send(ConsumerControlCode.VOLUME_INCREMENT)

            elif shortcut in ["volume down", "volume_down"]:
                cc.send(ConsumerControlCode.VOLUME_DECREMENT)

            else:
                keys = shortcut.replace("+", " ").replace("-", " ").split()
                combo = []
                for k in keys:
                    if k in modifier_map:
                        combo.append(modifier_map[k])
                    elif k in key_map:
                        combo.append(key_map[k])
                if combo:
                    keyboard.press(*combo)
                    keyboard.release_all()

        prev_states[i] = btn.value
    time.sleep(0.1)

