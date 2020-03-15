# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 06:32:54 2020

@author: Dell
"""
import glob
import sys
import os
from PIL import Image, ImageTk
try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

def vp_start_gui():
    '''Starting point when module is the main routine.'''
    root = tk.Tk()
    top = Toplevel1 (root)
    root.mainloop()


class Toplevel1:
    def __init__(self, top=None):

        top.geometry("710x450+333+128")
        top.minsize(120, 1)
        top.maxsize(1364, 749)
        top.resizable(1, 1)
        top.title("SmrtSummry")
        top.configure(background="#d9d9d9")

 
        #Canvas showing summary image           
        self.canvas = tk.Canvas(top)
        self.canvas.place(relx=0.028, rely=0.022, relwidth=0.5, relheight=0.878)    
        self.img = Image.open("summary.png")
        self.img = self.img.resize((157, 1080), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(self.img)  
        self.canvas.create_image(10,10, image=self.img)  
        self.canvas.image = self.img   

        #Listbox showing all frames
        self.Scrolledlistbox1 = tk.Listbox(top)       
        self.Scrolledlistbox1.place(relx=0.563, rely=0.022, relheight=0.878, relwidth=0.142)
        self.scrollbar = tk.Scrollbar(top,command=self.Scrolledlistbox1.yview)
        self.scrollbar.pack( side = tk.RIGHT, fill = tk.Y )       
        self.Scrolledlistbox1.configure(yscrollcommand=self.scrollbar.set)
        #double click on item in listbox to show item on small canvas        
        self.Scrolledlistbox1.bind("<Double-Button-1>", self.showimg)
        #loop to show files in listbox    
        self.path = 'frames'
        self.fpath = glob.glob('%s\\*.jpg'%self.path)
        for x in range(len(self.fpath)):
            self.Scrolledlistbox1.insert(tk.END, "frame{0}.jpg".format(x))


        #Small canvas to show frames
        self.S_canvas = tk.Canvas(top)
        self.S_canvas.place(relx=0.720, rely=0.022, relheight=0.250, relwidth=0.250)                  
            
        #Split Video button
        self.Button2 = tk.Button(top)
        self.Button2.place(relx=0.803, rely=0.3, height=24, width=85)
        self.Button2.configure(text='''Split video''')
        
        #Scanline Crop
        self.Button_scan = tk.Button(top)
        self.Button_scan.place(relx=0.803, rely=0.4, height=24, width=85)
        self.Button_scan.configure(text='''Scanline crop''')
        
        #Get Summary Button
        self.Button1 = tk.Button(top)
        self.Button1.place(relx=0.803, rely=0.5, height=24, width=85)
        self.Button1.configure(text='''Get summary''')

    def showimg(self,z):
        x = self.Scrolledlistbox1.get(tk.ANCHOR)
        self.img = Image.open("frames/%s"%x)
        self.img = self.img.resize((400, 200), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(self.img)  
        self.S_canvas.create_image(0,0, image=self.img, anchor="nw")  
        self.S_canvas.image = self.img  
        print(x,z)


if __name__ == '__main__':
    vp_start_gui()





