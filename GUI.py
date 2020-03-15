from SmrtSummary import SmrtSummary
import glob
import cv2 as cv
import datetime
from PIL import Image, ImageTk
import tkinter.filedialog
try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk
def vp_start_gui():
    '''Starting point when module is the main routine.'''
    root = tk.Tk()
    top = Toplevel1 (root)
    root.mainloop()
#Scan line selection
def new_window():
    global var,rx,ry,row,cols,canvas
    size = 600
    im = cv.imread("frames/frame0.jpg",cv.IMREAD_COLOR)
    cols = im.shape[1]#vertical pixels
    row = im.shape[0] #horizontal pixels 
    
    rx = int(cols)/size#Image size on x or width / image resize
    ry = int(row)/size#Image size on y or hieght / image resize
    
    
    var = tk.IntVar()
    root = tk.Toplevel()
    root.geometry("600x600+500+80")
    root.title("Scanline")
    root["bg"] = "navy"
    canvas = tk.Canvas(root)
    canvas.place(width=size, height=size)
    img = Image.open("frames/frame0.jpg")
    img = img.resize((size, size), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)  
    canvas.create_image(0,0, image=img, anchor="nw")  
    canvas.image = img  
    
    slider = tk.Scale(root, from_=0, to=cols,variable = var,  orient=tk.HORIZONTAL)
    slider.pack(side = tk.BOTTOM, fill = tk.X)
    button = tk.Button(root, text="Select scanline", command=sel)
    button.pack(anchor=tk.CENTER)  
def sel():
    global selection
    selection = int(var.get())
    rcol = selection/rx
    rrow = row/ry
    canvas.create_line(int(rcol), 0, int(rcol), rrow, fill="red", width=3)
    print(selection,int(rcol),rrow)
    return selection
#Instance of the video
def Video_window():
    global Vvar,Vrow,Vcols,Vcanvas
    im = cv.imread("summary.png",cv.IMREAD_COLOR)
    Vcols = im.shape[1]#vertical pixels
    Vrow = im.shape[0] #horizontal pixels 
    Vvar = tk.IntVar()
    root = tk.Toplevel()
    root.geometry("157x600+500+80")
    root.title("Image Summary")
    Vcanvas = tk.Canvas(root)
    Vcanvas.place(width=Vrow, height=1080)
    img = Image.open("summary.png")
    img = ImageTk.PhotoImage(img)  
    Vcanvas.create_image(0,0, image=img, anchor="nw")  
    Vcanvas.image = img  
    scrollbar = tk.Scrollbar(root,command=Vcanvas.yview)
    scrollbar.pack( side = tk.RIGHT, fill = tk.Y )       
    Vcanvas.config(yscrollcommand=scrollbar.set)     
    slider = tk.Scale(root, from_=0, to=Vcols,variable = Vvar, orient=tk.HORIZONTAL)
    slider.pack(side = tk.BOTTOM, fill = tk.X)
    button = tk.Button(root, text="Select line", command=Vsel)
    button.pack(anchor=tk.CENTER)    
def Vsel():
    Vselection = int(Vvar.get())
    Vcanvas.create_line(int(Vselection), 0, int(Vselection), Vrow, fill="red", width=3)
    print(Vselection,Vcols,Vrow)
    timestamp = Vselection/30
    print(str(datetime.timedelta(seconds=timestamp)))
class Toplevel1:
    ss = SmrtSummary()#SmrtSummary object 
    def __init__(self, top=None):

        top.geometry("710x450+333+128")
        top.minsize(120, 1)
        top.maxsize(1364, 749)
        top.resizable(1, 1)
        top.title("SmrtSummary")
        top.configure(background="#d9d9d9")

 
        #Canvas showing summary image           
        self.canvas = tk.Canvas(top)
        self.canvas.place(relx=0.028, rely=0.022, relwidth=0.5, relheight=0.878)    

        #Listbox showing all frames
        self.Scrolledlistbox1 = tk.Listbox(top)       
        self.Scrolledlistbox1.place(relx=0.563, rely=0.022, relheight=0.878, relwidth=0.142)
        self.scrollbar = tk.Scrollbar(top,command=self.Scrolledlistbox1.yview)
        self.scrollbar.pack( side = tk.RIGHT, fill = tk.Y )       
        self.Scrolledlistbox1.configure(yscrollcommand=self.scrollbar.set)
        #double click on item in listbox to show item on small canvas        
        self.Scrolledlistbox1.bind("<Double-Button-1>", self.C2_showimg)
        #loop to show files in listbox    
        self.path = 'frames'
        self.fpath = glob.glob('%s\\*.jpg'%self.path)
        #Small canvas to show frames
        self.S_canvas = tk.Canvas(top)
        self.S_canvas.place(relx=0.720, rely=0.022, relheight=0.250, relwidth=0.250)        
        #Load video
        self.Button_load = tk.Button(top,command=self.fileDialog)
        self.Button_load.place(relx=0.803, rely=0.3, height=24, width=85)
        self.Button_load.configure(text='''Load video''')
        
        self.label1 = tk.Label(top, text = "")
        self.label1.place(relx=0.720, rely=0.36, height=12, relwidth=0.250)
        #Split Video button
        self.Button2 = tk.Button(top,command=self.fun1)
        self.Button2.place(relx=0.803, rely=0.4, height=24, width=85)
        self.Button2.configure(text='''Split video''')        
        #Select scanline Button
        self.Button_scan = tk.Button(top,command=lambda: new_window())
        self.Button_scan.place(relx=0.803, rely=0.5, height=24, width=85)
        self.Button_scan.configure(text='''Select scanline''')
        #Get Summary Button
        self.Button1 = tk.Button(top,command=self.fun2)
        self.Button1.place(relx=0.803, rely=0.6, height=24, width=85)
        self.Button1.configure(text='''Get summary''')
        #Get video Button
        self.Button_video = tk.Button(top,command=lambda:Video_window())
        self.Button_video.place(relx=0.803, rely=0.7, height=24, width=85)
        self.Button_video.configure(text='''Open video''')
    #view frame in canvas
    def C2_showimg(self,z):
        x = self.Scrolledlistbox1.get(tk.ANCHOR)
        self.img = Image.open("frames/%s"%x)
        self.img = self.img.resize((400, 200), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(self.img)  
        self.S_canvas.create_image(0,0, image=self.img, anchor="nw")  
        self.S_canvas.image = self.img  
        print(x,z)
    #Show summary in canvas
    def C1_showimg(self):
            self.img = Image.open("summary.png")
            self.img = self.img.resize((157, 1080), Image.ANTIALIAS)
            self.img = ImageTk.PhotoImage(self.img)  
            self.canvas.create_image(10,10, image=self.img)  
            self.canvas.image = self.img  
            print("added to canvas")        
    #loop to show files in listbox          
    def fList(self):
        for x in range(len(self.fpath)):
            self.Scrolledlistbox1.insert(tk.END, "frame{0}.jpg".format(x))
            
    def fun1(self):
        l = self.label1['text']
        tkinter.messagebox.showinfo(title="Please Wait", message="Don't close any windows, video is proccessing")
        print(l)
        self.ss.split(l)
        print("aaaaa")
        self.fList()

    def fun2(self):
        self.ss.scanline(int(selection))
        print("scanline Done!")
        self.ss.image_Summary()
        print("image_Summary Done!")
        self.C1_showimg()
        
        
    def fileDialog(self):     
        self.filename = tk.filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("mp4 files","*.mp4"),("all files","*.*")))
        print(self.filename)
        self.label1.configure(text = self.filename)
        return self.filename
if __name__ == '__main__':
    vp_start_gui()





