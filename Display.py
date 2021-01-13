import tkinter as tk
from tkinter.ttk import *
from tkinter import messagebox as msg
from tkinter.ttk import Notebook
from tkinter import filedialog
from tkinter import ttk

import tkinter.messagebox as tkmsg
from PIL import Image, ImageTk, ImageDraw, ExifTags, ImageColor,ImageFont

import platform
import ImgViewer.imgview as IV
import aws_rekognition.rekognition as AWSRK 

class TestTool(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Test Tool Platform:"+str(platform.system()))        

        w = 600 # width for the Tk root
        h = 900 # height for the Tk root

        # get screen width and height
        ws = self.winfo_screenwidth() # width of the screen
        hs = self.winfo_screenheight() # height of the screen

        # calculate x and y coordinates for the Tk root window
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)

        # set the dimensions of the screen 
        # and where it is placed
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))

        '''self.notebook'''
        self.notebook = Notebook(self)
        self.notebook.pack(side = tk.TOP,fill=tk.BOTH, expand=tk.YES)

        self.init_ImgViewer()
        self.init_aws_rekognition_tab()
       
    def init_ImgViewer(self):
        self.init_ImgViewer_tab = tk.Frame(self.notebook)
        self.init_ImgViewer_tab.pack(side = tk.LEFT, expand=tk.YES, fill=tk.BOTH)
        self.notebook.add(self.init_ImgViewer_tab, text="init_ImgViewer")

        self.ImgSwitch = tk.StringVar()
        #self.ImgSelect = 

        ivfram1 = tk.Frame(self.init_ImgViewer_tab )
        ivfram1.grid(row =0, column = 0, sticky = tk.E+tk.W)
        self.iv1 = IV.ImageViewer(ivfram1)
        ivfram1_2 = tk.Frame(self.init_ImgViewer_tab )
        ivfram1_2.grid(row =0, column = 1, sticky = tk.E+tk.W)        

        opendir1 = tk.Button(ivfram1_2, text = "Open\n dir 1",font=('Courier', 9), command = self.iv1.open_dir)
        opendir1.pack(side=tk.TOP, expand=tk.YES, fill = tk.X)
        switch1 = tk.Radiobutton(ivfram1_2, text = "Img\n Switch 1",font=('Courier', 9), variable = self.ImgSwitch, value = "Img Switch 1", command = self.imgswitch)
        switch1.pack(side=tk.TOP, expand=tk.YES, fill = tk.X)
        
        ivfram2 = tk.Frame(self.init_ImgViewer_tab )
        ivfram2.grid(row =1, column = 0, sticky = tk.E+tk.W)
        self.iv2 = IV.ImageViewer(ivfram2)
        ivfram2_2 = tk.Frame(self.init_ImgViewer_tab )
        ivfram2_2.grid(row =1, column = 1, sticky = tk.E+tk.W)        
        
        opendir2 = tk.Button(ivfram2_2, text = "Open\n dir 2",font=('Courier', 9), command = self.iv2.open_dir)
        opendir2.pack(side=tk.TOP, expand=tk.YES, fill = tk.X)
        switch2 = tk.Radiobutton(ivfram2_2, text = "Img\n Switch 2",font=('Courier', 9), variable = self.ImgSwitch, value = "Img Switch 2", command = self.imgswitch)
        switch2.pack(side=tk.TOP, expand=tk.YES, fill = tk.X)

        select = tk.Checkbutton(self.init_ImgViewer_tab , text = "Select Image to compare ",font=('Courier', 9), command = self.imgselect)
        select.grid(row =2, column = 0, sticky = tk.E+tk.W)

    def imgswitch(self):
        if self.ImgSwitch.get() =="Img Switch 1": imageFile = self.iv1.image_paths[self.iv1.image_idx]
        elif self.ImgSwitch.get() =="Img Switch 2": imageFile = self.iv2.image_paths[self.iv2.image_idx]
        #elif self.ImgSwitch.get() =="Img Switch 3": imageFile = self.iv3.image_paths[self.iv3.image_idx]
        #elif self.ImgSwitch.get() =="Img Switch 4": imageFile = self.iv4.image_paths[self.iv4.image_idx]        
        self.awsrk.imageFile = imageFile

    def imgselect(self):
        imageFile1 = self.iv1.image_paths[self.iv1.image_idx]
        imageFile2 = self.iv2.image_paths[self.iv2.image_idx]
        self.awsrk.imageFile1 = imageFile1
        self.awsrk.imageFile2 = imageFile2

    def init_aws_rekognition_tab(self):
        self.aws_rekognition_tab = tk.Frame(self.notebook)
        #self.aws_rekognition_tab.grid(row =0, column = 0)
        self.notebook.add(self.aws_rekognition_tab, text="AWS Rekognition")
        self.awsrk = AWSRK.awsrekognition(self.aws_rekognition_tab)
        

if __name__ == "__main__":
       
    TT = TestTool()
    TT.mainloop()


