from baccarat.baccarat import BaccaratGui
from CustomUIfiles import BaccaratFiche
import PySide6.QtWidgets as QtWidgets
import sys
import os



class CasinoTestWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()



        self.central_widget = QtWidgets.QWidget()

        self.resize(1000, 700)
        self.setCentralWidget(self.central_widget)

        self.bfiche = BaccaratFiche()
        self.bfiche.SetOneValueFiche()
        self.bfiche.setParent(self)
        self.bfiche.show()




def main():
    app = QtWidgets.QApplication(sys.argv)
    ui  = CasinoTestWindow()
    ui.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    
    print("Working dir:", os.getcwd())  # Debug
    print("Image exists?", os.path.exists("src/extrafiles/baccaratImage/1casinochip.jpg"))
    main()