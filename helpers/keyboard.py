from pynput.keyboard import Key, Controller

_keyboard = Controller()

def press(key):
    _keyboard.press(key)
    _keyboard.release(key)