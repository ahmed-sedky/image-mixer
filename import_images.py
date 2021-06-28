import matplotlib.image as mpimg
from numpy import asarray
from PyQt5.QtWidgets import QFileDialog
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
from error_msg import error
import cv2

class image():
    def imp_image(self):
        path_image = QFileDialog.getOpenFileName(None, 'Open JPEG ', '/home', "JPEG (*.jpeg)")[0]
        return path_image
    def get_image_array(self):
        #img = matplotlib.image.imread(self.imp_image())
        #try:
        path=self.imp_image()
        #error().error_if_not_equal([1,2],[1,2],len(path))
        img = mpimg.imread(path)
        imgByte = cv2.imread(path, flags=cv2.IMREAD_GRAYSCALE).T

        data = asarray(img)
        return data,len(path),imgByte

    def get_2arrays(self):
        try:
            data1,path1,imb1=self.get_image_array()
            data2,path2,imb2=self.get_image_array()
            return data1,path1,imb1,data2,path2,imb2
        except Exception:
            pass
        #print(data1,data2)
        return 0,0,0,0,0,0
    def reshape(self,data,shape_of_data):
        data_shaped = data.reshape(shape_of_data)
        return data_shaped
    
