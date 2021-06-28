import numpy as np
from scipy.fft import fft, fftfreq,ifft,fftshift,ifftshift,rfft,rfftfreq,irfft
import matplotlib.pyplot as plt
from skimage.color import rgb2gray

class fourier():
    def data_processing(self,data):
        data=np.real(data)
        data=np.round(data)
        return data.astype(np.uint8)
    def get_fourier(self,data):
        data=fft(data)
        return data
    def get_inverse(self,data):
        data=ifft(data)
        return self.data_processing(data)
    def get_Magnitude(self,gain,data):
        data = np.abs(data)*gain
        return data
    def get_phase(self,gain,data):
        data=np.angle(data)*gain
        return data
    def get_real(self,gain,data):
        data=np.real(data)*gain
        return data
    def get_imag(self,gain,data):
        data=np.imag(data)*gain*1j
        return data
    def get_uniMag(self,data):
        data = np.abs(data)*0+1
        return data
    def get_uniPhase(self,data):
        data = np.angle(data)*0
        return data

    def data_mixing(self,list_data):
        list_components={
                        "Mag":{"Phase":[(self.get_Magnitude(list_data[0],list_data[4])+(self.get_Magnitude(1-list_data[0],list_data[5]))),self.get_phase(list_data[1],list_data[5])+self.get_phase(1-list_data[1],list_data[4])],"Uni Phase":[(self.get_Magnitude(list_data[0],list_data[4])+(self.get_Magnitude(1-list_data[0],list_data[5]))),self.get_uniPhase(list_data[5])]},
                        "Phase":{"Mag":[(self.get_Magnitude(list_data[1],list_data[5])+(self.get_Magnitude(1-list_data[1],list_data[4]))),self.get_phase(list_data[0],list_data[4])+self.get_phase(1-list_data[0],list_data[5])],"Uni Mag":[self.get_uniMag(list_data[5]),(self.get_phase(list_data[0],list_data[4])+(self.get_phase(1-list_data[0],list_data[5])))]},
                        "Uni Mag":{"Phase":[self.get_uniMag(list_data[4]),self.get_phase(list_data[1],list_data[5])+self.get_phase(1-list_data[1],list_data[4])],"Uni Phase":[self.get_uniMag(list_data[4]),self.get_uniPhase(list_data[5])]},
                        "Uni Phase":{"Mag":[(self.get_Magnitude(list_data[1],list_data[5])+(self.get_Magnitude(1-list_data[1],list_data[4]))),self.get_uniPhase(list_data[5])],"Uni Mag":[self.get_uniMag(list_data[5]),self.get_uniPhase(list_data[5])]},
                        "Real":{"Imag":[(self.get_real(list_data[0],list_data[4])+(self.get_real(1-list_data[0],list_data[5]))),self.get_imag(list_data[1],list_data[5])+self.get_imag(1-list_data[1],list_data[4])]},
                        "Imag":{"Real":[(self.get_real(list_data[1],list_data[5])+(self.get_real(1-list_data[1],list_data[4]))),self.get_imag(list_data[0],list_data[4])+self.get_imag(1-list_data[0],list_data[5])]}
                        }
        try:
            if list_data[2]=="Mag" or list_data[2]=="Phase" or list_data[2]=="Uni Mag" or list_data[2]=="Uni Phase":
                data_combined = np.multiply(list_components[list_data[2]][list_data[3]][0], np.exp(1j*list_components[list_data[2]][list_data[3]][1]))
            else:
                data_combined=np.array(list_components[list_data[2]][list_data[3]][0])+np.array(list_components[list_data[2]][list_data[3]][1])
            data_inverse=self.get_inverse(data_combined)
        except Exception:
            pass
        return data_inverse
    
    def choose_image_sequence(self,gain1,gain2,component1,component2,chooesed1,choosed2,data1,data2):
        self.image_sequence={"image1" : {"image 2":[gain1,gain2,chooesed1,choosed2,data1,data2],"image 1":[gain1,gain2,chooesed1,choosed2,data1,data1]},
              "image 2" : {"image 1":[gain1,gain2,chooesed1,choosed2,data2,data1],"image 2":[gain1,gain2,chooesed1,choosed2,data2,data2]}}
        return self.data_mixing(self.image_sequence[component1][component2])
    def rgb_to_gray(self,rgb):
        gray =rgb2gray(rgb)  
        f=np.fft.fft2(gray)
        fshift = np.fft.fftshift(f)
        return  fshift

    def image_components(self,choosed_component,data):
        FT_components={
            "magnitude":[20*np.log(self.get_Magnitude(1,self.rgb_to_gray(data)))],
            "phase":[self.get_phase(1,self.rgb_to_gray(data))],
            "real":[self.data_processing(20*np.log(np.real(self.rgb_to_gray(data))))],
            "imag":[self.data_processing(np.imag(self.rgb_to_gray(data)))],
        }
        return FT_components[choosed_component][0]