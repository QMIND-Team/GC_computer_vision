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
                self.getValues.emit([2,0,3,0,0])




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
   	    PString=""
   	    NumString=""
   	    CostString=""
   	    totalPrice=0
   	    ApplePrice=1.50
   	    OrangePrice=1.00
   	    BananaPrice=1.25
   	    appleTotal=0

   	    bananaTotal=0
   	    orangeTotal=0
   	    #apple id 53
   	    #banana id 52
   	    #orange 55
   	    TotalPrice=0
   	    UnitCostString=""
   	    Equals=""
   	    Times=""

   	    for i in range(0,len(value)):
   	        if (value[i] > 0):
   	            if i == 0:
   	                PString+="Apple\n"
   	                appleTotal=ApplePrice*value[i]
   	                TotalPrice+=appleTotal
   	                NumString+=str(value[i])+"\n"
   	                CostString+=str(appleTotal)+"\n"
   	                UnitCostString+=str(ApplePrice)+"\n"
   	                Times+="X\n"
   	                Equals+="=\n"

   	            if i == 1:
   	                PString+="Orange\n"
   	                orangeTotal=OrangePrice*value[i]
   	                TotalPrice+=orangeTotal
   	                NumString+=str(value[i])+"\n"
   	                CostString+=str(orangeTotal)+"\n"
   	                UnitCostString+=str(OrangePrice)+"\n"
   	                Times+="X\n"
   	                Equals+="=\n"

   	            if i == 2:
   	                PString+="Banana\n"
   	                bananaTotal=BananaPrice*value[i]
   	                TotalPrice+=bananaTotal
   	                NumString+=str(value[i])+"\n"
   	                CostString+=str(bananaTotal)+"\n"
   	                UnitCostString+=str(BananaPrice)+"\n"
   	                Times+="X\n"
   	                Equals+="=\n"

   	    self.itemDyP.setText(PString)
   	    self.numDyP.setText(NumString)
   	    self.timesP.setText(Times)
   	    self.costDyP.setText(UnitCostString)
   	    self.equalsP.setText(Equals)

   	    self.tcostDyP.setText(CostString)
   	    self.gtcostDyP.setText(str(TotalPrice))
        
    def initUI(self):

        self.item = QLabel('Item')
        self.num = QLabel('Number')
        self.cost = QLabel('Unit Cost')
        self.tcost = QLabel('Total Cost')
        self.gtcost = QLabel('Grand Total Cost')

        hori = QHBoxLayout()
        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(self.item, 0, 0)
        grid.addWidget(self.num, 0, 1)
        grid.addWidget(self.cost, 0, 3)
        grid.addWidget(self.tcost, 0, 5)
        grid.addWidget(self.gtcost, 0, 6)
        self.itemDyP = QLabel("")
        self.numDyP = QLabel("")
        self.costDyP = QLabel("")
        self.timesP = QLabel("")
        self.equalsP = QLabel("")
        self.tcostDyP = QLabel("")
        self.gtcostDyP = QLabel("")

        grid.addWidget(self.itemDyP, 1, 0, 3, 1)
        grid.addWidget(self.numDyP, 1, 1, 3, 1)
        grid.addWidget(self.timesP, 1, 2, 3, 1)
        grid.addWidget(self.costDyP, 1, 3, 3, 1)
        grid.addWidget(self.equalsP, 1, 4, 3, 1)
        grid.addWidget(self.tcostDyP, 1, 5, 3, 1)
        grid.addWidget(self.gtcostDyP, 1, 6, 3, 1)
        self.label = QLabel(self)
        self.label.resize(300,300)
        hori.addWidget(self.label)
        hori.addLayout(grid)
        self.setLayout(hori)
        self.setWindowTitle(self.title)
        self.setGeometry(300, 300, 600, 400)
        
        #self.label = QLabel(self)
        #self.label.move(280, 120)
        #self.label.resize(300,300)

        self.show()
        th = Thread(self)
        th.changePixmap.connect(self.setImage)
        th.getValues.connect(self.getClasses)
        th.start()



if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())