import cv2
import sys
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, 
    QTextEdit, QGridLayout, QApplication, QHBoxLayout)
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, Qt




class Thread(QThread):
    changePixmap = pyqtSignal(QImage)
    getValues = pyqtSignal(object)

    def run(self):
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if ret:
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                convertToQtFormat = QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0], QImage.Format_RGB888)
                p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)
                self.getValues.emit([0,0,0,0,0])




class Example(QWidget):
    
    def __init__(self):
        super().__init__()
        self.title = "Grocery Checkout"
        self.initUI()
        
    @pyqtSlot(QImage)
    def setImage(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))

    @pyqtSlot(object)
    def getClasses(self, value):
    	 print("List: {}".format(value))
        
    def initUI(self):
        '''
        item = QLabel('Item')
        num = QLabel('Number')
        cost = QLabel('Unit Cost')
        tcost = QLabel('Total Cost')

        hori = QHBoxLayout()

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(item, 0, 0)
        grid.addWidget(num, 0, 1)
        grid.addWidget(cost, 0, 3)
        grid.addWidget(tcost, 0, 5)
        
        

        
        itemDyP = QLabel("Patel's Dal Tadka Lentil Curry")
        numDyP = QLabel("0")
        costDyP = QLabel("$3.50")
        timesP = QLabel("X")
        equalsP = QLabel("=")
        tcostDyP = QLabel("0")
        grid.addWidget(itemDyP, 1, 0, 3, 1)
        grid.addWidget(numDyP, 1, 1, 3, 1)
        grid.addWidget(timesP, 1, 2, 3, 1)
        grid.addWidget(costDyP, 1, 3, 3, 1)
        grid.addWidget(equalsP, 1, 4, 3, 1)
        grid.addWidget(tcostDyP, 1, 5, 3, 1)

        itemDyA = QLabel("Annie's Snicker Doodle")
        numDyA = QLabel("0")
        costDyA = QLabel("$3.50")
        timesA = QLabel("X")
        equalsA = QLabel("=")
        tcostDyA = QLabel("0")
        grid.addWidget(itemDyA, 2, 0, 3, 1)
        grid.addWidget(numDyA, 2, 1, 3, 1)
        grid.addWidget(timesA, 2, 2, 3, 1)
        grid.addWidget(costDyA, 2, 3, 3, 1)
        grid.addWidget(equalsA, 2, 4, 3, 1)
        grid.addWidget(tcostDyA, 2, 5, 3, 1)

        itemDyC = QLabel("Blue Diamond Nut Thins Almond Cheddar")
        numDyC = QLabel("0")
        costDyC = QLabel("$3.50")
        timesC = QLabel("X")
        equalsC = QLabel("=")
        tcostDyC = QLabel("0")
        grid.addWidget(itemDyC, 3, 0, 3, 1)
        grid.addWidget(numDyC, 3, 1, 3, 1)
        grid.addWidget(timesC, 3, 2, 3, 1)
        grid.addWidget(costDyC, 3, 3, 3, 1)
        grid.addWidget(equalsC, 3, 4, 3, 1)
        grid.addWidget(tcostDyC, 3, 5, 3, 1)

        itemDyS = QLabel("Blue Diamond Nut Thins Almond Seasalt")
        numDyS = QLabel("0")
        costDyS = QLabel("$3.50")
        timesS = QLabel("X")
        equalsS = QLabel("=")
        tcostDyS = QLabel("0")
        grid.addWidget(itemDyS, 4, 0, 3, 1)
        grid.addWidget(numDyS, 4, 1, 3, 1)
        grid.addWidget(timesS, 4, 2, 3, 1)
        grid.addWidget(costDyS, 4, 3, 3, 1)
        grid.addWidget(equalsS, 4, 4, 3, 1)
        grid.addWidget(tcostDyS, 4, 5, 3, 1)

        itemDyH = QLabel("Higgins and Burke Naturals")
        numDyH = QLabel("0")
        costDyH = QLabel("$3.50")
        timesH = QLabel("X")
        equalsH = QLabel("=")
        tcostDyH = QLabel("0")
        grid.addWidget(itemDyH, 5, 0, 3, 1)
        grid.addWidget(numDyH, 5, 1, 3, 1)
        grid.addWidget(timesH, 5, 2, 3, 1)
        grid.addWidget(costDyH, 5, 3, 3, 1)
        grid.addWidget(equalsH, 5, 4, 3, 1)
        grid.addWidget(tcostDyH, 5, 5, 3, 1)
        
        itemDyH = QLabel("Final Total")
        tcostDyF = QLabel("0")
        grid.addWidget(itemDyH, 6, 0, 3, 1)
        
        grid.addWidget(tcostDyF, 6, 5, 3, 1)

        #hori.addStretch(1)
        hori.addLayout(grid)

        self.setLayout(hori) 
        
        self.setGeometry(300, 300, 600, 400)
        self.setWindowTitle('Grocery Checkout')    
        self.show()
        '''

        self.item = QLabel('Item')
        self.num = QLabel('Number')
        self.cost = QLabel('Unit Cost')
        self.tcost = QLabel('Total Cost')

        hori = QHBoxLayout()
        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(self.item, 0, 0)
        grid.addWidget(self.num, 0, 1)
        grid.addWidget(self.cost, 0, 3)
        grid.addWidget(self.tcost, 0, 5)
        hori.addLayout(grid)
        self.setLayout(hori)
        self.setWindowTitle(self.title)
        self.setGeometry(300, 300, 600, 400)
        
        self.label = QLabel(self)
        self.label.move(280, 120)
        self.label.resize(640, 480)

        self.show()
        th = Thread(self)
        th.changePixmap.connect(self.setImage)
        th.getValues.connect(self.getClasses)
        th.start()



if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())