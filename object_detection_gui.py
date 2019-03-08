import sys
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, 
    QTextEdit, QGridLayout, QApplication, QHBoxLayout)
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, Qt
import numpy as np
import tensorflow as tf
import cv2
import time

class DetectorAPI:
    def __init__(self, path_to_ckpt):
        self.path_to_ckpt = path_to_ckpt

        self.detection_graph = tf.Graph()
        with self.detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(self.path_to_ckpt, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')

        self.default_graph = self.detection_graph.as_default()
        self.sess = tf.Session(graph=self.detection_graph)

        # Definite input and output Tensors for detection_graph
        self.image_tensor = self.detection_graph.get_tensor_by_name('image_tensor:0')
        # Each box represents a part of the image where a particular object was detected.
        self.detection_boxes = self.detection_graph.get_tensor_by_name('detection_boxes:0')
        # Each score represent how level of confidence for each of the objects.
        # Score is shown on the result image, together with the class label.
        self.detection_scores = self.detection_graph.get_tensor_by_name('detection_scores:0')
        self.detection_classes = self.detection_graph.get_tensor_by_name('detection_classes:0')
        self.num_detections = self.detection_graph.get_tensor_by_name('num_detections:0')

    def processFrame(self, image):
        # Expand dimensions since the trained_model expects images to have shape: [1, None, None, 3]
        image_np_expanded = np.expand_dims(image, axis=0)
        # Actual detection.
        start_time = time.time()
        (boxes, scores, classes, num) = self.sess.run(
            [self.detection_boxes, self.detection_scores, self.detection_classes, self.num_detections],
            feed_dict={self.image_tensor: image_np_expanded})
        end_time = time.time()

        print("Elapsed Time:", end_time - start_time)

        im_height, im_width, _ = image.shape
        boxes_list = [None for i in range(boxes.shape[1])]
        for i in range(boxes.shape[1]):
            boxes_list[i] = (int(boxes[0, i, 0] * im_height),
                             int(boxes[0, i, 1] * im_width),
                             int(boxes[0, i, 2] * im_height),
                             int(boxes[0, i, 3] * im_width))

        return boxes_list, scores[0].tolist(), [int(x) for x in classes[0].tolist()], int(num[0])

    def close(self):
        self.sess.close()
        self.default_graph.close()

class Thread(QThread):
    changePixmap = pyqtSignal(QImage)
    getValues = pyqtSignal(object)

    def run(self):
        # change model_path
        model_path = r'ssd_mobilenet_v2_coco_2018_03_29/frozen_inference_graph.pb'
        odapi = DetectorAPI(path_to_ckpt=model_path)
        threshold = 0.60
        label_prev = np.zeros(90)

        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            boxes, scores, classes, num = odapi.processFrame(frame)
            labels = np.zeros(90)
            for i in range(len(boxes)):
                for label in range(len(labels)):
                    if classes[i] == label and scores[i] > threshold and (classes[i] in [52,53,55]):
                        box = boxes[i]
                        cv2.rectangle(frame, (box[1], box[0]), (box[3], box[2]), (255, 0, 0), 2)
                        labels[label] += 1
                        print(label)
            # print(labels)

            old_labels = labels


            if ret:
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                convertToQtFormat = QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0], QImage.Format_RGB888)
                p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)

                self.changePixmap.emit(p)
                self.getValues.emit(labels)




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
                if i == 53:
                    PString+="Apple\n"
                    appleTotal=ApplePrice*value[i]
                    TotalPrice+=appleTotal
                    NumString+=str(value[i])+"\n"
                    CostString+=str(appleTotal)+"\n"
                    UnitCostString+=str(ApplePrice)+"\n"
                    Times+="X\n"
                    Equals+="=\n"

                if i == 55:
                    PString+="Orange\n"
                    orangeTotal=OrangePrice*value[i]
                    TotalPrice+=orangeTotal
                    NumString+=str(value[i])+"\n"
                    CostString+=str(orangeTotal)+"\n"
                    UnitCostString+=str(OrangePrice)+"\n"
                    Times+="X\n"
                    Equals+="=\n"

                if i == 52:
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