from baccarat.baccarat import BaccaratGui
import PySide6.QtWidgets as Qt
import sys

def main():
    app = Qt.QApplication(sys.argv)
    ui  = BaccaratGui()
    ui.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
