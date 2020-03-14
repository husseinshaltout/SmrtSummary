# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 02:34:30 2020

@author: Hussein Shaltout
"""

import cv2
import os
class SmrtSummary:
    def __init__(self):
        cap= cv2.VideoCapture('test.mp4')
        path = 'C:/Users/Dell/Documents/GitHub/SmrtSummary/frames'
    def split(self):
        i=0
        while(self.cap.isOpened()):
            ret, frame = self.cap.read()
            if ret == False:
                break            
            cv2.imwrite(os.self.path.join(self.path , 'frame'+str(i)+'.jpg'), frame)
            i+=1        
        self.cap.release()
        cv2.destroyAllWindows()
    def start(self):
        self.split()
if __name__ == "__main__":
    SmrtSummary = SmrtSummary()        
    SmrtSummary.start()
        
        
        
        
# =============================================================================
# # Opens the Video file
# cap= cv2.VideoCapture('test.mp4')
# 
# path = 'C:/Users/Dell/Documents/GitHub/SmrtSummary/frames'
# 
# i=0
# while(cap.isOpened()):
#     ret, frame = cap.read()
#     if ret == False:
#         break
#     # cv2.imwrite('kang'+str(i)+'.jpg',frame)
#     cv2.imwrite(os.path.join(path , 'frame'+str(i)+'.jpg'), frame)
#     i+=1
#  
# cap.release()
# cv2.destroyAllWindows()
# =============================================================================
