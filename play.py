from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Key, Controller as KeyboardController

import time
import json
import threading

import global_vars



class Play:
    """
    This class is responsible for playing back recorded mouse and keyboard events.

    Attributes:
        SPECIAL_KEYS (dict): A dictionary mapping special key names to their corresponding pynput Key objects.
        ASCII_TO_CHAR (dict): A dictionary mapping ASCII control characters to their corresponding characters.
                                The reason I use ASCII_TO_CHAR because self.keyboard.press('\x01') not run even though it's not buggy.
    
    Methods:
        __init__(self, file_name="record.json", number_of_play=1): Initialize the Play instance.
        load(self): Load recorded events from a JSON file.
        play(self): Start playing back the recorded events in a separate thread.
        _play(self): Internal method for actually playing back the events.
    """


    SPECIAL_KEYS = {"Key.shift": Key.shift, "Key.tab": Key.tab, "Key.caps_lock": Key.caps_lock, "Key.ctrl_l": Key.ctrl_l, "Key.alt_l": Key.alt_l, "Key.cmd": Key.cmd, "Key.cmd_r": Key.cmd_r, "Key.alt_r": Key.alt_r, "Key.ctrl_r": Key.ctrl_r, "Key.shift_r": Key.shift_r, "Key.enter": Key.enter, "Key.backspace": Key.backspace, "Key.f19": Key.f19, "Key.f18": Key.f18, "Key.f17": Key.f17, "Key.f16": Key.f16, "Key.f15": Key.f15, "Key.f14": Key.f14, "Key.f13": Key.f13, "Key.media_volume_up": Key.media_volume_up, "Key.media_volume_down": Key.media_volume_down, "Key.media_volume_mute": Key.media_volume_mute, "Key.media_play_pause": Key.media_play_pause, "Key.f6": Key.f6, "Key.f5": Key.f5, "Key.right": Key.right, "Key.down": Key.down, "Key.left": Key.left, "Key.up": Key.up, "Key.page_up": Key.page_up, "Key.page_down": Key.page_down, "Key.home": Key.home, "Key.end": Key.end, "Key.delete": Key.delete, "Key.space": Key.space}
    ASCII_TO_CHAR = {'\x01': 'a', '\x02': 'b', '\x03': 'c', '\x04': 'd', '\x05': 'e', '\x06': 'f', '\x07': 'g', '\x08': 'h', '\x09': 'i', '\x0a': 'j', '\x0b': 'k', '\x0c': 'l', '\x0d': 'm', '\x0e': 'n', '\x0f': 'o', '\x10': 'p', '\x11': 'q', '\x12': 'r', '\x13': 's', '\x14': 't', '\x15': 'u', '\x16': 'v', '\x17': 'w', '\x18': 'x', '\x19': 'y', '\x1a': 'z',}


    def __init__(self):
        """
        Initialize the Play instance.

        Args:
            file_name (str, optional): The name of the JSON file containing recorded events. Default is "record.json".
            number_of_play (int, optional): The number of times to play back the recorded events. Default is 1.
        """

        self.mouse = MouseController()
        self.keyboard = KeyboardController()
        self.data = None
        self.thread_play = None
        

    def load(self, file_name= "record.json"):
        """
        Load recorded events from a JSON file.
        """

        with open(f"data/{file_name}") as json_file:
            self.data = json.load(json_file)
    
    def play(self):
        """
        Start playing back the recorded events in a separate thread.
        """
        
        self.thread_play = threading.Thread(target=self._play ,daemon= True)
        self.thread_play.start()

    def join(self):
        self.thread_play.join()

    def _play(self):
        """
        Internal method for actually playing back the recorded events.
        """

        for index, event in enumerate(self.data):
            
            if global_vars.play_end:
                return

            action = event["action"]
            _time = event["_time"]

            try:
                interval = self.data[index + 1]["_time"] - _time
            except IndexError:
                interval = 1

            # Handle event keyboard
            if action == "pressed_key" or action == "released_key":
                if "Key." in event['key']:
                    key = Play.SPECIAL_KEYS[event['key']]
                elif "\\" in ascii(event['key']):
                    try:
                        key = Play.ASCII_TO_CHAR[event['key']]
                    except KeyError:
                        key = event['key']
                else :
                    key = event['key']

                print(f"action: {action}, time: {_time}, key: {ascii(key)}")

                if action == "pressed_key":
                    self.keyboard.press(key)
                elif action == "released_key":
                    self.keyboard.release(key)

                time.sleep(interval)

            # Handle event mouse
            else:
                x, y = event['x'], event['y']

                print(f"action: {action}, x: {x}, y: {y}, time: {_time}")

                self.mouse.position = (x, y)

                if action == "pressed":
                    self.mouse.press(Button.left if event['button'] == "Button.left" else Button.right)
                elif action == "released":
                    self.mouse.release(Button.left if event['button'] == "Button.left" else Button.right)
                elif action == "scroll":
                    horizontal_direction = event['horizontal_direction']
                    vertical_direction = event['vertical_direction']
                    self.mouse.scroll(horizontal_direction, vertical_direction)
                time.sleep(interval)
        
        # global_vars.play_end = True


if __name__ == "__main__":
    player = Play()
    player.load("keyboard_record.json")
    player.play()
    player.join()
