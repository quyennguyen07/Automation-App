from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt6.QtGui import QIcon
import sys

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Đặt tiêu đề cửa sổ
        self.setWindowTitle("Ứng dụng có icon")

        # Tạo một đối tượng QIcon từ file hình ảnh
        icon = QIcon("icon_auto.jpg")  # Thay "path_to_your_icon.png" bằng đường dẫn đến file hình ảnh icon của bạn

        # Đặt icon cho cửa sổ
        self.setWindowIcon(icon)

        # Tạo một nút có chữ "Click me"
        button = QPushButton("Click me", self)
        button.setGeometry(50, 50, 100, 30)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())
