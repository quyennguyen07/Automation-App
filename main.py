"""
Main Script

This script demonstrates how to use the Record and Play classes along with the PyQt6 library
to create a simple application for recording and playing back mouse and keyboard events.

Usage:
    Run this script to start the graphical application. Use the GUI to record and play
    back mouse and keyboard events.

Author:
    Nguyen Dinh Quyen
"""



from PyQt6.QtWidgets import QApplication
from mainwindow import MainWindow

from record import Record
from play import Play
from browser import Browser
import global_vars
from keyboard_check import KeyboardCheck
import sys


class RecorderController:
    def __init__(self, recorder: object, window: object):
        self.recorder = recorder
        self.window = window
    
    def start_record(self, broswer):
        path_profile = self.window.ui.record_path_profile_edit.text()
        url = window.ui.record_url_edit.text()
        print(url)

        if path_profile and url:
            broswer.open("TEST", path_profile)
            broswer.access_website(url)
        
        self.recorder.start()

    def stop_record(self):
        self.recorder.save()
        self.recorder.stop()

    def save_record(self):
        self.recorder.save(self.window.file_save)



class PlayerController:
    def __init__(self, player: object):
        self.player = player

    def start_play(self, window, browser, keyboard_check):
        path_profile = window.ui.record_path_profile_edit.text()
        url = window.ui.play_url_edit.text()
        iteration_value = window.ui.iteration_spin.value()
        file_record = window.ui.file_record_edit.text()
        print(iteration_value, url, file_record)

        keyboard_check.listen()

        for i in range(1, iteration_value + 1):
            if not global_vars.play_end:
                if path_profile and url:
                    browser.open(f"Profile {i}", path_profile)
                    browser.access_website(url)
                self.player.load(file_record)
                self.player.play()
                self.player.join()
                if path_profile and url:
                    browser.close()

        keyboard_check.stop()
        window.showNormal()
        global_vars.play_end = False
        print("Play End")


def set_play_end_to_true():
    global_vars.play_end = True


if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = MainWindow()

    broswer = Browser("Chrome")
    recorder = Record()
    player = Play()
    keyboard_check = KeyboardCheck(func= set_play_end_to_true)

    recorder_controller = RecorderController(recorder, window)
    player_controller = PlayerController(player)


    window.connect_record_button(func=recorder_controller.start_record, args=(broswer,))
    window.connect_stop_button(func=recorder_controller.stop_record)
    window.connect_save_button(func=recorder_controller.save_record)
    window.connect_play_button(func=player_controller.start_play, args=(window, broswer, keyboard_check,))


    window.show()
    sys.exit(app.exec())

