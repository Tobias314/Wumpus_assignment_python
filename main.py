import sys
from PyQt5.QtWidgets import QApplication, QWidget

from gui.mainwindow import MainWindow



def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.setMinimumSize(700, 700)
    window.show()  # IMPORTANT!!!!! Windows are hidden by default.

    # Start the event loop.
    app.exec_()



if __name__ == '__main__':
    main()