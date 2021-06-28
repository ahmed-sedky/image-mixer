import sys
from PyQt5 import QtWidgets as qtw
from mixergui import Ui_MainWindow
from import_images import image
from error_msg import error
from fourier_Trans import fourier
import numpy as np
import logging
class MainWindow(qtw.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.show()
        ls=["Phase","Uni Phase"]
        self.label_list=[self.ui.gain1,self.ui.gain2]
        self.ui.comboBox_component_choose2.addItems(ls)
        self.ui.actionnew_file.triggered.connect(self.open_newwindow)
        self.ui.actionopen_images.triggered.connect(self.getdata)
        for i in range(1,len(self.ui.list_combobox)):
            self.ui.list_combobox[i].currentTextChanged.connect(self.gain)
        for i in range(len(self.ui.list_sliders)):
            self.ui.list_sliders[i].sliderReleased.connect(self.gain)
        for i in range(len(self.ui.list_combobox_image_component)):
            self.ui.list_combobox_image_component[i].currentTextChanged.connect(self.view_component)
        self.ui.list_combobox[0].currentTextChanged.connect(self.disbale_option)
    def disbale_option(self):
        self.ui.comboBox_component_choose2.clear()
        self.ui.comboBox_component_choose2.addItems(self.ui.complex_combinations[self.ui.comboBox_component_choose1.currentText()])
        self.ui.comboBox_component_choose2.setCurrentIndex(0)
        self.gain()
    def view_component(self):
        try:
            for i in range(2):
                self.gray=fourier().image_components(self.ui.list_combobox_image_component[i].currentText(),self.data_list_timedomain[i])
                self.draw_label(self.gray,i+2)
        except Exception:
            pass
    def gain(self):
        try:
            error().error_if_not_equal(self.data1,self.data2)
            for i in range(2):
                self.label_list[i].setText(str(self.ui.list_sliders[i].value()))
            #self.ui.gain1.setText(str(self.ui.list_sliders[0].value()))
            #self.ui.gain2.setText(str(self.ui.list_sliders[1].value()))
            self.data_mixed=fourier().choose_image_sequence(self.ui.list_sliders[0].value()/100,self.ui.list_sliders[1].value()/100,self.ui.list_combobox[2].currentText(),self.ui.list_combobox[3].currentText(),self.ui.list_combobox[0].currentText(),self.ui.list_combobox[1].currentText(),self.data_list[0],self.data_list[1])
            if self.ui.list_combobox[4].currentText()=='output1':
                self.draw_label(image().reshape(self.data_mixed,self.data_shape),4)
            else:
                self.draw_label(image().reshape(self.data_mixed,self.data_shape),5)
        except Exception: 
            pass
    def get_fourier_list(self,i):
        self.data_list[i]=fourier().get_fourier(self.data_list[i].reshape(-1))
    def draw_label(self,data,i):
        self.ui.figurs_list[i].clear()
        ax=self.ui.figurs_list[i].add_subplot(111)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.imshow(data,cmap="gray")
        self.ui.figurs_list[i].canvas.draw()
    def getdata(self):
        self.data1,path1,self.data1_timedomain,self.data2,path2,self.data2_timedomain=image().get_2arrays()
        try:
            error().error_if_not_equal(self.data1,self.data2,path1,path2)
            self.data_shape=self.data1.shape
            self.data_list=[self.data1,self.data2]
            self.data_list_timedomain=[self.data1_timedomain,self.data2_timedomain]
            for i in range(2):
                self.draw_label(self.data_list[i],i)
                self.get_fourier_list(i)
            self.gain()
            self.view_component()
        except Exception:
            pass
    def open_newwindow(self):
        self.new_instance = MainWindow()
        self.new_instance.show()
if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    app.setStyle("Fusion")
    mw = MainWindow()
    sys.exit(app.exec_())
