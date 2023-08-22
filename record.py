from pynput import mouse, keyboard
import json
import time
import global_vars

class Record:
    """
    A class for recording and saving mouse and keyboard events.

    This class provides the ability to start and stop recording of both mouse and keyboard events,
    and save the recorded events to a JSON file.

    Attributes:
        mouse_recorder (MouseRecord): An instance of MouseRecord for recording mouse events.
        keyboard_recorder (KeyboardRecord): An instance of KeyboardRecord for recording keyboard events.

    Methods:
        __init__(self): Initialize the Record instance.
        start(self): Start recording mouse and keyboard events.
        stop(self): Stop recording mouse and keyboard events.
        save(self, file_name="record"): Save the recorded events to a JSON file.

    Example:
        # Create a Record object
        record = Record()

        # Start recording mouse and keyboard events
        record.start()

        # Perform actions to record events

        # Stop recording
        record.stop()

        # Save the recorded events to a JSON file
        record.save("my_record")
    """

    def __init__(self):
        """
        Initialize the Record instance.
        """
        self.storage = []
        self.mouse_recorder = MouseRecord()
        self.keyboard_recorder = KeyboardRecord()

    
    def start(self):
        """
        Initialize the Record instance.

        This method initializes the mouse_recorder and keyboard_recorder attributes.
        """

        self.mouse_recorder.listen()
        self.keyboard_recorder.listen()

    def stop(self):
        """
        Stop recording mouse and keyboard events.

        This method stops listening to both mouse and keyboard events, ending the recording.
        """

        self.mouse_recorder.stop()
        self.keyboard_recorder.stop()
        

    def save(self, file_name= "record"):
        """
        Save the recorded events to a JSON file.

        Args:
            file_name (str, optional): The name of the JSON file. Default is "record".
        """

        self.storage = self.mouse_recorder.storage + self.keyboard_recorder.storage
        self.storage.sort(key= lambda x: x["_time"])

        with open(f"data/{file_name}.json", 'w') as out_file:
            json.dump(self.storage, out_file, indent= 4)

      


class MouseRecord:
    """
    A class for recording mouse events.

    This class provides methods to record mouse movement, clicks, and scrolls, and save them to a JSON file.

    Methods:
        __init__(self): Initialize the MouseRecord instance.
        _on_move(x, y): Handle the mouse move event and store it in the storage list.
        _on_click(x, y, button, pressed): Handle the mouse click event and store it in the storage list.
        _on_scroll(x, y, dx, dy): Handle the mouse scroll event and store it in the storage list.
        save(self, file_name="mouse_record"): Save the recorded mouse events to a file.
        listen(self): Start listening to mouse events and recording them.
        stop(self): Stops the recording of mouse events.

    Attributes:
        storage (list): A list to store recorded mouse events in JSON format.

    Example:
        # Create a MouseRecord object
        mouse_recorder = MouseRecord()

        # Start recording mouse events
        mouse_recorder.listen()

        # Perform mouse actions to record events

        # Stop recording
        mouse_recorder.stop()

        # Save the recorded mouse events to a JSON file
        mouse_recorder.save("my_mouse_record")
    """
    
    def __init__(self):
        """
        Initialize the MouseRecord instance.

        This method initializes the storage list and sets up the mouse listener.
        """
        
        self.storage = []
        self.mouse_listener = None
       

    def _on_move(self, x, y):
        """
        Handle the mouse move event and store it in the storage list.

        Args:
            x (int): The x-coordinate of the mouse cursor.
            y (int): The y-coordinate of the mouse cursor.
        """

        json_object = {'action': 'moved', 'x': x, 'y': y, '_time': time.time()}
        self.storage.append(json_object)
        print(json_object)


    def _on_click(self, x, y, button, pressed):
        """
        Handle the mouse click event. If record_all is True, store the event in the storage list.

        Args:
            x (int): The x-coordinate of the mouse cursor.
            y (int): The y-coordinate of the mouse cursor.
            button (Button): The button that was clicked (left, right, middle).
            pressed (bool): True if the button was pressed, False if it was

        Returns:
            bool: False to stop the mouse listener if a right-click is detected for more than 2 seconds, otherwise True.
        """
        
        json_object = {'action': 'pressed' if pressed else 'released',
                        'button': str(button), 
                        'x': x, 
                        'y': y, 
                        '_time': time.time()}
        self.storage.append(json_object)

        print(json_object)
        
        if self.storage[-1]['action'] == 'released' and self.storage[-1]['button'] == 'Button.right' and self.storage[-1]['_time'] - self.storage[-2]['_time'] > 2:
            return False


    def _on_scroll(self, x, y, dx, dy):
        """
        Handle the mouse scroll event. If record_all is True, store the event in the storage list.

        Args:
            x (int): The x-coordinate of the mouse cursor.
            y (int): The y-coordinate of the mouse cursor.
            dx (int): The horizontal scroll distance.
            dy (int): The vertical scroll distance.

        """

        json_object = {'action': 'scroll', 'vertical_direction': int(dy), 'horizontal_direction': int(dx), 'x': x, 'y': y, '_time': time.time()}
        self.storage.append(json_object)

        print(json_object)


    def save(self, file_name = "mouse_record"):
        """
        Save the recorded mouse events to a file.

        Args:
            file_name (str, optional): The name of the file. Default is "mouse_record".
        """

        with open(f"data/{file_name}.json", 'w') as outfile:
            json.dump(self.storage, outfile)


    def listen(self):
        """
        Starts listening to mouse events and recording them.

        # self.mouse_listener.join() is used to wait for the completion of the recording 
        before continuing to execute other commands so if you turn on it, file main.py will 
        not run app if be recorded. You should just turn on in file record.py to test.
        """
        self.storage = []
        self.mouse_listener = mouse.Listener(
                            on_click=self._on_click, 
                            on_scroll=self._on_scroll, 
                            on_move=self._on_move
                        )
        self.mouse_listener.start()
        # self.mouse_listener.join()


    def stop(self):
        """
        Stops the recording of mouse events.
        """

        self.mouse_listener.stop()




class KeyboardRecord:
    """
    A class for recording keyboard events and saving them to a JSON file.

    This class provides methods to record key presses and releases, and save them to a JSON file.

    Attributes:
        storage (list): A list to store the recorded keyboard events as JSON objects.

    Methods:
        __init__(self): Initialize the KeyboardRecord instance.
        _on_press(key): Callback method to be executed when a key is pressed.
        _on_release(key): Callback method to be executed when a key is released.
        save(self, file_name="keyboard_record"): Saves the recorded keyboard events to a JSON file.
        listen(self): Start listening to keyboard events and recording them.
        stop(self): Stops the recording of keyboard events.

    Example:
        # Create a KeyboardRecord object
        keyboard_recorder = KeyboardRecord()

        # Start recording keyboard events
        keyboard_recorder.listen()

        # Perform key presses and releases to record events

        # Stop recording
        keyboard_recorder.stop()

        # Save the recorded keyboard events to a JSON file
        keyboard_recorder.save("my_keyboard_record")
    """


    def __init__(self):
        """
        Initialize the KeyboardRecord instance.

        This method initializes the storage list and sets up the keyboard listener.
        """

        self.storage = []
        self.keyboard_listener = None

    def _on_press(self, key):
        """
        Callback method to be executed when a key is pressed.

        This method handles the 'pressed_key' event and records it in the storage list.

        Args:
            key (pynput.keyboard.Key or pynput.keyboard.KeyCode): The key object representing the pressed key.

        Returns:
            bool: False if the escape key is pressed (to stop the keyboard listener), otherwise None.
        """

        try:
            json_object = {'action':'pressed_key', 'key':key.char, '_time': time.time()}
        except AttributeError:
            if key == keyboard.Key.esc:
                return False
            print("ok")
            json_object = {'action':'pressed_key', 'key':str(key), '_time': time.time()}
            
        print(json_object)
        self.storage.append(json_object)


    def _on_release(self, key):
        """
        Callback method to be executed when a key is released.

        This method handles the 'released_key' event and records it in the storage list.

        Args:
            key (pynput.keyboard.Key or pynput.keyboard.KeyCode): The key object representing the released key.
        """

        try:
            json_object = {'action':'released_key', 'key':key.char, '_time': time.time()}
        except AttributeError:
            json_object = {'action':'released_key', 'key':str(key), '_time': time.time()}

        print(json_object)
        self.storage.append(json_object)


    def save(self, file_name= "keyboard_record"):
        """
        Saves the recorded keyboard events to a JSON file.

        Args:
            file_name (str, optional): The name of the JSON file. Default is "keyboard_record".
        """
        
        with open(f"data/{file_name}.json", 'w') as outfile:
            json.dump(self.storage, outfile)


    def listen(self):
        """
        Start listening to keyboard events and recording them.

        # self.keyboard_listener.join() is used to wait for the completion of the recording 
        before continuing to execute other commands so if you turn on it, file main.py will 
        not run app if be recorded. You should just turn on in file record.py to test.
        """
        self.storage = []
        self.keyboard_listener = keyboard.Listener(
                                    on_press=self._on_press,
                                    on_release=self._on_release,
                                )
        
        self.keyboard_listener.start()
        self.keyboard_listener.join()


    def stop(self):
        """
        Stops the recording of keyboard events.
        """

        self.keyboard_listener.stop()

        


if __name__ == "__main__":
    """
    Example usage of the Record, MouseRecord, and KeyboardRecord classes.
    """

    keyboard_recorder = KeyboardRecord()

    keyboard_recorder.listen()

    name_of_recording = "keyboard_record"
    keyboard_recorder.save(name_of_recording)
