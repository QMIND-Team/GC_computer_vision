# Code adapted from Tensorflow Object Detection Framework
# https://github.com/tensorflow/models/blob/master/research/object_detection/object_detection_tutorial.ipynb
# Tensorflow Object Detection Detector

import numpy as np
import tensorflow as tf
import cv2
import time

cap = cv2.VideoCapture(0)
class DetectorAPI:
    def __init__(self, path_to_ckpt):
        self.path_to_ckpt = path_to_ckpt


        # initialize a graph
        self.detection_graph = tf.Graph()
        # sets to default graph
        with self.detection_graph.as_default():
            # https://github.com/tensorflow/tensorflow/blob/r1.12/tensorflow/core/framework/graph.proto
            od_graph_def = tf.GraphDef()
            # some sort of file wrapping of current model
            with tf.gfile.GFile(self.path_to_ckpt, 'rb') as fid:
                # get file content as a string
                serialized_graph = fid.read()
                # parse the string
                od_graph_def.ParseFromString(serialized_graph)
                # imports the specified graph into the default graph
                tf.import_graph_def(od_graph_def, name='')


        # NOTE: At this point the graph has been loaded from checkpoint that was specified


        # returns a context manager to default_graph, not sure what that means
        self.default_graph = self.detection_graph.as_default()
        # create a session with the detection_graph
        self.sess = tf.Session(graph=self.detection_graph)

        # this specifies all of the operations that are being seeked
        # Definite input and output Tensors for detection_graph
        self.image_tensor = self.detection_graph.get_tensor_by_name('image_tensor:0')
        # Each box represents a part of the image where a particular object was detected.
        self.detection_boxes = self.detection_graph.get_tensor_by_name('detection_boxes:0')
        # Each score represent how level of confidence for each of the objects.
        # Score is shown on the result image, together with the class label.
        self.detection_scores = self.detection_graph.get_tensor_by_name('detection_scores:0')
        self.detection_classes = self.detection_graph.get_tensor_by_name('detection_classes:0')
        self.num_detections = self.detection_graph.get_tensor_by_name('num_detections:0')

        # NOTE: All of these operation should theoretically return some type of tensor

    def processFrame(self, image):
        # Expand dimensions since the trained_model expects images to have shape: [1, None, None, 3]
        image_np_expanded = np.expand_dims(image, axis=0)
        # Actual detection.
        start_time = time.time()

        # The session is run, printing this, the session would return the tensors collected by the image_tensor:0
        # operation and others, since they are run in a list the output is a list which is then passed to the tuple
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
        # closes the session
        self.sess.close()
        self.default_graph.close()


if __name__ == "__main__":
    model_path = r'C:\models\research\object_detection\SSD_resnet50_FPN_GC3\frozen_inference_graph.pb'
    odapi = DetectorAPI(path_to_ckpt=model_path)
    threshold = 0.60
    label_prev = np.zeros(5)

    while True:
        r, image = cap.read()
        boxes, scores, classes, num = odapi.processFrame(image)
        # Visualization of the results of a detection.
        labels = np.zeros(5)
        for i in range(len(boxes)):
            for label in range(len(labels)):
                if classes[i] == label and scores[i] > threshold:
                    box = boxes[i]
                    cv2.rectangle(image, (box[1], box[0]), (box[3], box[2]), (255, 0, 0), 2)
                    labels[label] += 1
        print(labels)

        # TODO call function to update

        old_labels = labels
        # delete row from csv at (count)

        # delete blank rows from deleted csv rows

        cv2.imshow('object detection', image)
        key = cv2.waitKey(25)
        if key & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break