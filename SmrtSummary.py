# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 02:34:30 2020

@author: Hussein Shaltout
"""
import numpy as np
import cv2 as cv
import os
import glob

class SmrtSummary:
    def __init__(self):
        self.cap= cv.VideoCapture('test.mp4')
        self.path = 'C:/Users/Dell/Documents/GitHub/SmrtSummary/frames'
        self.path1 = 'C:/Users/Dell/Documents/GitHub/SmrtSummary/frames/cropped'
    def split(self):
        i=0
        while(self.cap.isOpened()):
            ret, frame = self.cap.read()
            if ret == False:
                break            
            cv.imwrite(os.path.join(self.path , 'frame'+str(i)+'.jpg'), frame)
            i+=1        
        self.cap.release()
        cv.destroyAllWindows()
        
    def readLine(self):
        img_array = []
        # im = cv.imread("frames/frame0.jpg",cv.IMREAD_COLOR)        
        # rows = im.shape[0]        
        # cropped = im[0:rows, 1000:1100]
        k = glob.glob('C:\\Users\\Dell\\Documents\\GitHub\\SmrtSummary\\frames\\*.jpg')
        
        for filename in glob.glob('C:\\Users\\Dell\\Documents\\GitHub\\SmrtSummary\\frames\\*.jpg'):
            # print(filename)
            im = cv.imread(filename,cv.IMREAD_COLOR)
            rows = im.shape[0]        
            cropped = im[0:rows, 1000:1100]             
            cv.imwrite(os.path.join(self.path1 , filename.split("\\")[-1]), cropped)
        
        for filename in range(len(k)):
            img = cv.imread(filename)
            height, width, layers = img.shape
            size = (width,height)
            img_array.append(img)
        print(img_array)
        out = cv.VideoWriter('project.avi',cv.VideoWriter_fourcc(*'DIVX'), 30, size)
        for i in range(len(img_array)):
            out.write(img_array[i])
        out.release()
        # cv.imwrite("thumbnail.png", numpy_horizontal)
        # return im
        
    def show_wait_destroy(self, winname, img):
        cv.imshow(winname, img)
        cv.moveWindow(winname, 500, 0)
        cv.waitKey(0)
        cv.destroyWindow(winname)        
    def start(self):
        # self.split()`
        self.readLine()
        # self.show_wait_destroy("test", self.readLine())
if __name__ == "__main__":
    SmrtSummary = SmrtSummary()        
    SmrtSummary.start()
        
        
        
        
