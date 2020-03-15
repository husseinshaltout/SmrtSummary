# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 02:34:30 2020

@author: Hussein
"""
import numpy as np
import cv2 as cv
import os
import glob

class SmrtSummary:
    def __init__(self):
        #Splitted frames from video location
        self.path = 'frames'
        #cropped files location
        self.C_path = '%s/cropped'%self.path
        #All files with extension jpeg in frames folder
        self.fpath = glob.glob('%s\\*.jpg'%self.path)
    #Function to split video into frames
    def split(self,l):
        self.cap= cv.VideoCapture(l)
        i=0
        while(self.cap.isOpened()):
            ret, frame = self.cap.read()
            if ret == False:
                break            
            cv.imwrite(os.path.join(self.path , 'frame'+str(i)+'.jpg'), frame)
            print("Splitting Frame #%s"%str(i))
            i+=1        
        self.cap.release()
        cv.destroyAllWindows()
        
    def scanline(self,x): 
        #Crop all frames with defined x value/line
        for filename in self.fpath:
            im = cv.imread(filename,cv.IMREAD_COLOR)
            rows = im.shape[0]        
            cropped = im[0:rows, x-1:x]  
            print(filename.split("\\")[-1])
            cv.imwrite(os.path.join(self.C_path , filename.split("\\")[-1]), cropped)
    
    def image_Summary(self):
        # Concatenate all cropped images horizontaly 
        for x in range(len(self.fpath)):
            print(os.path.join(self.C_path ,"frame{0}.jpg").format(x))
            if(x == 0):
                numpy_horizontal = cv.imread(os.path.join(self.C_path ,"frame{0}.jpg").format(x))
            else:
                img = cv.imread(os.path.join(self.C_path ,"frame{0}.jpg").format(x))
                numpy_horizontal = np.hstack((numpy_horizontal, img))
        #Create summary image
        cv.imwrite("summary.png", numpy_horizontal)
        
    def mvideo(self):
        img_array = []
        for x in range(len(self.fpath)):
            img = cv.imread(os.path.join(self.C_path ,"frame{0}.jpg").format(x))
            height, width, layers = img.shape
            size = (width,height)
            img_array.append(img)
        out = cv.VideoWriter('project.avi',cv.VideoWriter_fourcc(*'DIVX'), 30, size)
        for i in range(len(img_array)):
            out.write(img_array[i])
        out.release()
        
        
    def show_wait_destroy(self, winname, img):
        cv.imshow(winname, img)
        cv.moveWindow(winname, 500, 0)
        cv.waitKey(0)
        cv.destroyWindow(winname)        
    def start(self):
        # self.split()
        self.scanline()
        # self.image_Summary()
        # self.show_wait_destroy("test", self.readLine())
if __name__ == "__main__":
    SmrtSummary = SmrtSummary()        
    SmrtSummary.start()
        
        
        
        
