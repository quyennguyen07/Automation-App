from pynput import keyboard


class KeyboardCheck:
    """
    A class to monitor keyboard events and trigger a specified function when a certain key is pressed.

    This class creates a keyboard listener that can detect when a specific key is pressed, such as the ESC key,
    and then calls a provided function along with any associated arguments.

    Args:
        func (callable): The function to call when the specified key is pressed.
        args (tuple): Arguments to pass to the function when triggered.
    """


    def __init__(self, func = None, args= ()):
        
        self.keyboard_listener = None
        self.func = func
        self.args = args

    def check_key_ESC(self, key):
        """
        Check if the specified key is pressed and trigger the associated function.
        """

        if key == keyboard.Key.esc:
            self.func(*self.args)


    def listen(self):
        """
        Start listening for keyboard events.
        """
        self.keyboard_listener = keyboard.Listener(on_press= self.check_key_ESC)
        self.keyboard_listener.start()

    def stop(self):
        """
        Stop listening for keyboard events.
        """
        self.keyboard_listener.stop()