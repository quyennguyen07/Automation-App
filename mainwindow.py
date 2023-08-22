# This file is used to handle events on button

from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt6.QtCore import QTimer, QTime
from PyQt6.QtGui import QIcon

from ui_mainwindow1 import Ui_MainWindow
from keyboard_check import KeyboardCheck



class MainWindow(QMainWindow):
    """
    A class representing the main window of the application with interactive buttons and event handling.

    This class defines the main user interface window of the application. It creates and manages buttons,
    connects them to appropriate event handlers, and also includes methods to handle specific button clicks.
    """

    def __init__(self):

        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowIcon(QIcon("image/icon_auto.ico"))
        self.setWindowTitle("Automation App")

        # if keyboard = esc, click stop_button
        self.keyboard_check_when_recording = KeyboardCheck(func= self.ui.stop_button.click)


        # Timer on QLCDNumber
        self.timer = QTimer()
        self.start_time = None

        self.file_save = None
        
        self.ui.file_record_edit.setText("record.json")

        self.set_path_profile()

        self.ui.record_button.clicked.connect(self.on_record_key_click)
        self.ui.stop_button.clicked.connect(self.on_stop_button_click)
        self.ui.save_button.clicked.connect(self.update_file_save)
        self.ui.play_button.clicked.connect(self.on_play_button_click)




    def connect_record_button(self, func, args= ()):
        self.ui.record_button.clicked.connect(lambda: func(*args))
    def connect_stop_button(self, func, args= ()):
        self.ui.stop_button.clicked.connect(lambda: func(*args))
    def connect_save_button(self, func, args= ()):
        self.ui.save_button.clicked.connect(lambda: func(*args))
    def connect_play_button(self, func, args= ()):
        self.ui.play_button.clicked.connect(lambda: func(*args))


    def on_record_key_click(self):
        """
        Handle event when click record
        """
        self.start_recording()

        self.ui.record_button.setEnabled(False)
        self.ui.play_button.setEnabled(False)
        
        self.showMinimized()

        self.keyboard_check_when_recording.listen()
        
        self.save_record_path_profile()


    def on_stop_button_click(self):
        """
        Handle event when click stop
        """
        self.ui.record_button.setEnabled(True)
        self.ui.play_button.setEnabled(True)
        
        self.showNormal()

        self.keyboard_check_when_recording.stop()

        self.timer.timeout.disconnect(self.update_lcd_time)
        self.timer.stop()


    def on_play_button_click(self):
        """
        Handle event when click play
        """
        self.showMinimized()

        self.save_play_path_profile()


    def start_recording(self):
        self.start_time = QTime.currentTime()
        self.timer.timeout.connect(self.update_lcd_time)
        self.timer.start(1000)


    def update_lcd_time(self):
        if self.start_time:
            current_time = QTime.currentTime()
            elapsed_time = self.start_time.secsTo(current_time)
            minutes = elapsed_time // 60
            seconds = elapsed_time % 60
            self.ui.lcd_time.display(f"{minutes:02}:{seconds:02}")


    def update_file_save(self):
        file_path, _= QFileDialog.getSaveFileName(self, "Save File", "data/", "Json Files (*.json);;All Files (*)")
        self.file_save = file_path.rsplit("/", 1)[1].split(".")[0]


    def set_path_profile(self):
        try:
            with open("information/path_profile.txt", 'r') as file:
                path_profile = file.read()
                self.ui.record_path_profile_edit.setText(path_profile)
                self.ui.play_path_profile_edit.setText(path_profile)
        except FileNotFoundError:
            print("File not exits")
            

    def save_record_path_profile(self):
        with open("information/path_profile.txt", 'w') as file:
            file.write(self.ui.record_path_profile_edit.text())


    def save_play_path_profile(self):
        with open("information/path_profile.txt", 'w') as file:
            file.write(self.ui.play_path_profile_edit.text())


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())