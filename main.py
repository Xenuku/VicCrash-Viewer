# pyQt skeleton
import sys
from PyQt5.QtWidgets import QApplication, QWidget

def main():
    app = QApplication(sys.argv)
    main_window = QWidget()
    main_window.resize(1200, 800)
    main_window.move(30, 30)
    main_window.setWindowTitle('Visual Data, biatch!')
    main_window.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()