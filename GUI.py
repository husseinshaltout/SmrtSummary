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
def Video_window(vl):
    global Vvar,Vrx,Vry,Vrow,Vcols,Vcanvas,gVL
    gVL = vl
    vw = 160#Image resize and canvas width
    vh = 600#Image resize and canvas height
    Vrx = int(cols)/vw#Image size on x or width / image resize
    Vry = int(row)/vh#Image size on y or hieght / image resize
    if(len(gVL) == 0):
        tkinter.messagebox.showinfo(title="Get Summary", message="Please create video summary to play video")
    else:
        im = cv.imread("summary.png",cv.IMREAD_COLOR)
        Vcols = im.shape[1]#vertical pixels
        Vrow = im.shape[0] #horizontal pixels 
        Vvar = tk.IntVar()
        root = tk.Toplevel()
        root.geometry("157x600+500+80")
        root.title("Image Summary")
        Vcanvas = tk.Canvas(root)
        Vcanvas.place(width=vw, height=vh)
        img = Image.open("summary.png")
        img = img.resize((vw, vh), Image.ANTIALIAS)
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
    print(len(gVL))
def Vsel():
    Vselection = int(Vvar.get())
    rcol = Vselection/Vrx
    rrow = Vrow/Vry
    Vcanvas.create_line(int(rcol), 0, int(rcol), rrow, fill="red", width=3)
    print(Vselection,rcol,rrow)
    timestamp = Vselection/30
    ts = str(datetime.timedelta(seconds=timestamp))
    print(ts)
    tk.messagebox.showinfo(title="Play video", message="Timestamp: %s \n Press q to exit"%ts)
    print(gVL)
    video_play(Vselection,gVL)
def video_play(index,location):
    # Create a VideoCapture object and read from input file
    # If the input is the camera, pass 0 instead of the video file name
    cap = cv.VideoCapture(location)
    cap.set(cv.CAP_PROP_POS_FRAMES, index)
    # Check if camera opened successfully
    if (cap.isOpened()== False): 
      print("Error opening video stream or file")    
    # Read until video is completed
    while(cap.isOpened()):
      # Capture frame-by-frame
      ret, frame = cap.read()
      if ret == True:    
        # Display the resulting frame
        cv.namedWindow('Frame',cv.WINDOW_NORMAL)
        cv.resizeWindow('Frame', 600,600)
        cv.imshow('Frame',frame)
        cv.moveWindow('Frame', 500, 0)
        # Press Q on keyboard to  exit
        if cv.waitKey(25) & 0xFF == ord('q'):
          break    
      # Break the loop
      else: 
        break    
    # When everything done, release the video capture object
    cap.release()    
    # Closes all the frames
    cv.destroyAllWindows()    
class Toplevel1:    
    ss = SmrtSummary()#SmrtSummary object 
    def __init__(self, top=None):
        self.split_flag = 0
        self.scanline_flag = 0
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
        #Video location label        
        self.label1 = tk.Label(top, text = "")
        self.label1.place(relx=0.720, rely=0.36, height=12, relwidth=0.250)
        #Split Video button
        self.Button2 = tk.Button(top,command=self.fun1)
        self.Button2.place(relx=0.803, rely=0.4, height=24, width=85)
        self.Button2.configure(text='''Split video''')        
        #Select scanline Button
        self.Button_scan = tk.Button(top,command=lambda: self.callback())
        self.Button_scan.place(relx=0.803, rely=0.5, height=24, width=85)
        self.Button_scan.configure(text='''Select scanline''')
        #Get Summary Button
        self.Button1 = tk.Button(top,command=self.fun2)
        self.Button1.place(relx=0.803, rely=0.6, height=24, width=85)
        self.Button1.configure(text='''Get summary''')
        #Get video Button
        self.Button_video = tk.Button(top,command=lambda:Video_window(self.label1['text']))
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
    #get video location then split video then show frames in boxlist        
    def fun1(self): 
        print(len(self.fpath))
        l = self.label1['text']
        if(l ==""):
            tkinter.messagebox.showinfo(title="No video", message="Please select a video first")
        else:
            tkinter.messagebox.showinfo(title="Please Wait", message="Don't close any windows, video is proccessing")
            print(l)
            self.ss.split(l)
            print("aaaaa")
            self.fList()
            self.split_flag = 1
    #Newwindow callback with conditon
    def callback(self):
        if(self.split_flag == 0):
            tkinter.messagebox.showinfo(title="Split Video", message="Please split video first")
        else:
            new_window()
            self.scanline_flag = 1
    #Select scanline to crop and get video summary
    def fun2(self):        
        if(self.scanline_flag== 0):
            tkinter.messagebox.showinfo(title="No Scanline", message="Please select scanline")
        else:
            self.ss.scanline(int(selection))
            print("scanline Done!")
            self.ss.image_Summary()
            print("image_Summary Done!")
            self.C1_showimg()        
    #File dialog for browing to open video    
    def fileDialog(self):     
        self.filename = tk.filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("mp4 files","*.mp4"),("all files","*.*")))
        print(self.filename)
        self.label1.configure(text = self.filename)
if __name__ == '__main__':
    vp_start_gui()





