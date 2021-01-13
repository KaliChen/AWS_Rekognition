import requests
import boto3
import os
from os.path import splitext
import cv2
#import rtsp
import numpy as np
import time
from PIL import Image, ImageTk, ImageDraw, ExifTags, ImageColor,ImageFont
import tkinter.messagebox as tkmsg
import tkinter as tk
from tkinter.ttk import *
from tkinter import messagebox as msg
from tkinter.ttk import Notebook
from tkinter import filedialog
from tkinter import ttk
from tkinter.colorchooser import *
import json
fontofcv2_Item = {cv2.FONT_HERSHEY_SIMPLEX:'HERSHEY_SIMPLEX',cv2.FONT_HERSHEY_PLAIN:'HERSHEY_PLAIN', cv2.FONT_HERSHEY_DUPLEX:'HERSHEY_DUPLEX', 
                  cv2.FONT_HERSHEY_COMPLEX:'HERSHEY_COMPLEX',cv2.FONT_HERSHEY_TRIPLEX:'HERSHEY_TRIPLEX', cv2.FONT_HERSHEY_COMPLEX_SMALL:'HERSHEY_COMPLEX_SMALL',
                  cv2.FONT_HERSHEY_SCRIPT_SIMPLEX:'ERSHEY_SCRIPT_SIMPLEX', cv2.FONT_HERSHEY_SCRIPT_COMPLEX:'HERSHEY_SCRIPT_COMPLEX'} 
fontlinetype_Item = {cv2.LINE_AA:'LINE_AA',cv2.LINE_8:'LINE_8'}
fontsize = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 16, 20, 22, 24, 28, 32, 36, 40, 44, 48, 52, 54, 60, 72)
linewidth = ( 1, 2, 3, 4, 5)

class awsrekognition():
    def __init__(self, master):
        self.parent = master
        self.imageFile = str()
        self.imageFile1 = str()
        self.imageFile2 = str()
        
        self.color_1 = (0,0,0)
        self.color_2 = (0,0,0)
        self.awsrekognitionPanel = tk.LabelFrame(self.parent, text="AWS Rekognition",font=('Courier', 10))
        self.awsrekognitionPanel.pack(side=tk.LEFT, expand=tk.NO, fill = tk.X)
        self.init_aws_rekognition_tab()
        self.init_setting_tab()
        self.init_DisplaySceneMarkInfo_tab()
        

    def init_setting_tab(self):
        self.setting_tab = tk.Frame(self.awsrekognitionPanel)
        self.setting_tab.pack(side=tk.TOP, expand=tk.YES, fill=tk.BOTH)
        #self.settingnotebook.add(self.ColorDraw_tab, text = "Color&Draw")

        self.MarkSettingPanel = tk.LabelFrame(self.setting_tab, text="Setting Panel",font=('Courier', 10))
        self.MarkSettingPanel.pack(side=tk.TOP, expand=tk.YES, fill=tk.BOTH)

        '''Color Panel'''
        ColorPanel = tk.Frame(self.MarkSettingPanel)
        ColorPanel.grid(row = 0, column = 0 ,sticky = tk.E+tk.W)        
        self.Color1Button = tk.Button(ColorPanel, text = "Color 1",font=('Courier', 10), command = self.askcolor1)
        self.Color1Button.grid(row = 0, column = 0, sticky = tk.E+tk.W)
        self.Color2Button = tk.Button(ColorPanel, text = "Color 2",font=('Courier', 10), command = self.askcolor2)
        self.Color2Button.grid(row = 1, column = 0, sticky = tk.E+tk.W)

        '''font line type setting'''
        fontcv2Panel = tk.Frame(self.MarkSettingPanel)
        fontcv2Panel.grid(row = 0, column = 1 ,sticky = tk.E+tk.W, rowspan = 5)
        '''Font of cv2 label'''
        tk.Label(fontcv2Panel , text = "Font of cv2",font=('Courier', 10)).pack(side = tk.TOP, expand=tk.YES, fill=tk.BOTH)
        self.fontcv2Var = tk.IntVar()
        self.fontcv2Var.set(1)
        for val, fontcv2type, in fontofcv2_Item.items(): 
            tk.Radiobutton(fontcv2Panel, text = fontcv2type, variable = self.fontcv2Var, value = val,font=('Courier', 8)).pack(side = tk.TOP, expand=tk.YES, fill=tk.BOTH)

        '''Font Size'''
        tk.Label(self.MarkSettingPanel, text = "font size",font=('Courier', 10)).grid(row = 0, column = 2, sticky = tk.E+tk.W)
        #self.fontsizespinbox = tk.Spinbox(self.MarkSettingPanel, from_ = 1, to = 48, increment = 1, width = 3)
        self.fontsizespinbox = tk.Spinbox(self.MarkSettingPanel, values = fontsize, width = 3)
        self.fontsizespinbox.grid(row = 1, column = 2, sticky = tk.E+tk.W)
        '''Line Size'''
        tk.Label(self.MarkSettingPanel, text = "Line size",font=('Courier', 10)).grid(row = 2, column = 2, sticky = tk.E+tk.W)        
        #self.linesizespinbox = tk.Spinbox(self.MarkSettingPanel, from_ = 1, to = 10, increment = 1, width = 3)
        self.linesizespinbox = tk.Spinbox(self.MarkSettingPanel, values = linewidth,  width = 3)
        self.linesizespinbox.grid(row = 3, column = 2, sticky = tk.E+tk.W)

        '''font line type setting'''
        fontlinetypecv2Panel = tk.Frame(self.MarkSettingPanel)
        fontlinetypecv2Panel.grid(row = 4, column = 2 ,sticky = tk.E+tk.W)
        '''line type label'''
        tk.Label(fontlinetypecv2Panel, text = "line type",font=('Courier', 10)).pack(side = tk.TOP, expand=tk.YES, fill=tk.BOTH)       
        self.fontlinetypecv2Var = tk.IntVar()
        self.fontlinetypecv2Var.set(8)
        for val, linetype, in fontlinetype_Item.items(): 
            tk.Radiobutton(fontlinetypecv2Panel, text = linetype, variable = self.fontlinetypecv2Var, value = val,font=('Courier', 10)).pack(side = tk.TOP, expand=tk.YES, fill=tk.BOTH)

    def init_DisplaySceneMarkInfo_tab(self):
        self.DisplaySceneMarkInfo_Frame = tk.LabelFrame(self.awsrekognitionPanel, text="Display AWS Rekognition Info", font=('Courier', 10))
        self.DisplaySceneMarkInfo_Frame .pack(side=tk.TOP, expand=tk.NO)
        DisplaySceneMarkInfoCLEAR =tk.Button(self.awsrekognitionPanel, text = "Clear",font=('Courier', 10), command = self.DisplaySceneMarkInfoCLEAR)
        DisplaySceneMarkInfoCLEAR.pack(side=tk.TOP, expand=tk.YES)
        self.DisplaySceneMarkInfo = tk.Text(self.DisplaySceneMarkInfo_Frame, width = 50, height = 9) 
        DisplaySceneMarkInfo_sbarV = Scrollbar(self.DisplaySceneMarkInfo_Frame, orient=tk.VERTICAL)
        DisplaySceneMarkInfo_sbarH = Scrollbar(self.DisplaySceneMarkInfo_Frame, orient=tk.HORIZONTAL)
        DisplaySceneMarkInfo_sbarV.config(command=self.DisplaySceneMarkInfo.yview)
        DisplaySceneMarkInfo_sbarH.config(command=self.DisplaySceneMarkInfo.xview)
        self.DisplaySceneMarkInfo.config(yscrollcommand=DisplaySceneMarkInfo_sbarV.set)
        self.DisplaySceneMarkInfo.config(xscrollcommand=DisplaySceneMarkInfo_sbarH.set)
        DisplaySceneMarkInfo_sbarV.pack(side=tk.RIGHT, fill=tk.Y)
        DisplaySceneMarkInfo_sbarH.pack(side=tk.BOTTOM, fill=tk.X)
        self.DisplaySceneMarkInfo.pack(side=tk.TOP, expand=tk.NO)


    def DisplaySceneMarkInfoCLEAR(self, event = None):
        self.DisplaySceneMarkInfo.delete('1.0', tk.END)
        tkmsg.showinfo("Information","CLEAR")

    def askcolor1(self, event = None):
        self.color1 = askcolor()
        self.Color1Button.configure(bg=self.color1[1])
        self.color_1 = self.HTMLColorToRGB(self.color1[1])

    def askcolor2(self, event = None):
        self.color2 = askcolor()
        self.Color2Button.configure(bg=self.color2[1])
        self.color_2 = self.HTMLColorToRGB(self.color2[1])

    def HTMLColorToRGB(self,colorstring):
        """ convert #RRGGBB to an (R, G, B) tuple """
        colorstring = colorstring.strip()
        if colorstring[0] == '#': colorstring = colorstring[1:]
        if len(colorstring) != 6:
            raise(ValueError, "input #%s is not in #RRGGBB format" % colorstring)
        r, g, b = colorstring[:2], colorstring[2:4], colorstring[4:]
        r, g, b = [int(n, 16) for n in (r, g, b)]
        return (r, g, b)

    def init_aws_rekognition_tab(self):
        self.aws_rekognition_tab = tk.Frame(self.awsrekognitionPanel)
        self.aws_rekognition_tab.pack(side = tk.TOP, expand=tk.YES, fill=tk.BOTH)
        #self.imgfunnotebook.add(self.aws_rekognition_tab, text="AWS Rekognition")

        self.workonAWS_Face_rekoButton = tk.Button(self.aws_rekognition_tab, text = "Face Rekognition",font=('Courier', 8), command = self.face_rekognition)
        self.workonAWS_Face_rekoButton.pack(side=tk.LEFT, expand=tk.NO)
        self.workonAWS_Cele_rekoButton = tk.Button(self.aws_rekognition_tab, text = "Celebrities",font=('Courier', 8), command = self.celebrities)
        self.workonAWS_Cele_rekoButton.pack(side=tk.LEFT, expand=tk.NO)
        self.workonAWS_Label_rekoButton = tk.Button(self.aws_rekognition_tab, text = "Object and Animal",font=('Courier', 8), command = self.label_rekognition)
        self.workonAWS_Label_rekoButton.pack(side=tk.LEFT, expand=tk.NO)
        self.workonAWS_Text_rekoButton = tk.Button(self.aws_rekognition_tab, text = "Text",font=('Courier', 8), command = self.text_rekognition)
        self.workonAWS_Text_rekoButton.pack(side=tk.LEFT, expand=tk.NO)

        #self.localpicturename = tk.StringVar()

        #self.loadPicButton = tk.Button(self.aws_rekognition_tab, text = "Load Picture",font=('Courier', 8), command = self.load_picture)
        #self.loadPicButton.pack(side=tk.LEFT, expand=tk.NO, fill = tk.X)

        #self.needComparedPath = tk.Entry(self.aws_rekognition_tab , textvariable=self.localpicturename)
        #self.needComparedPath.pack(side=tk.LEFT, expand=tk.NO, fill = tk.X)

        self.workonAWS_Compare_rekoButton = tk.Button(self.aws_rekognition_tab, text = "Compare",font=('Courier', 8), command = self.Compare_rekognition)
        self.workonAWS_Compare_rekoButton.pack(side=tk.TOP, expand=tk.YES, fill = tk.X)


    def face_rekognition(self,event = None):

        client=boto3.client('rekognition')

        #self.imageFile = self.parent.imgswitch()

        #Call OpenCV Object img
        img = cv2.imread(self.imageFile)
        #img of PIL object
        img_PIL = Image.open(self.imageFile)
        #width, height, channels = img.shape  #20190506 the size of OpenCV object is not good to use :(
        width, height = img_PIL.size

        with open(self.imageFile, 'rb') as image:
            faces_response = client.detect_faces(Image={'Bytes': image.read()},Attributes=['ALL'])

        face_jsonfile = "faceoutput.json"
        with open(face_jsonfile, 'w') as fp:
            json.dump(faces_response, fp)

        imOut = img.copy()
        for faceDetail in faces_response['FaceDetails']:
            cv2.rectangle(imOut,
                              (int(width*faceDetail['BoundingBox']['Left']),
                               int(height*faceDetail['BoundingBox']['Top'])),
                               (int(width*(faceDetail['BoundingBox']['Left']+faceDetail['BoundingBox']['Width'])),
                               int(height*(faceDetail['BoundingBox']['Top']+faceDetail['BoundingBox']['Height']))),
                              self.color_1,int(self.linesizespinbox.get()))
            for eachperson in faceDetail['Landmarks']:
                cv2.circle(imOut, (int(width*eachperson['X']), int(height*eachperson['Y'])), int(self.linesizespinbox.get()), self.color_2, -1)

            self.DisplaySceneMarkInfo.insert(tk.END,'==========================================\n')
            self.DisplaySceneMarkInfo.insert(tk.END,'Age: '+str(faceDetail['AgeRange']['Low']) +' to '+str(faceDetail['AgeRange']['High'])+' years old\n')
            self.DisplaySceneMarkInfo.insert(tk.END,'Beard Confidence: '+str(faceDetail['Beard']['Confidence']) +' Value: '+str(faceDetail['Beard']['Value'])+'\n')
            self.DisplaySceneMarkInfo.insert(tk.END,'Eyeglasses Confidence: '+str(faceDetail['Eyeglasses']['Confidence']) +' Value: '+str(faceDetail['Eyeglasses']['Value'])+'\n')        
            self.DisplaySceneMarkInfo.insert(tk.END,'EyesOpen Confidence: '+str(faceDetail['EyesOpen']['Confidence']) +' Value: '+str(faceDetail['EyesOpen']['Value'])+'\n')
            self.DisplaySceneMarkInfo.insert(tk.END,'Gender Confidence: '+str(faceDetail['Gender']['Confidence']) +' Value: '+str(faceDetail['Gender']['Value'])+'\n')
            self.DisplaySceneMarkInfo.insert(tk.END,'MouthOpen Confidence: '+str(faceDetail['MouthOpen']['Confidence']) +' Value: '+str(faceDetail['MouthOpen']['Value'])+'\n')
            self.DisplaySceneMarkInfo.insert(tk.END,'Mustache Confidence: '+str(faceDetail['Mustache']['Confidence']) +' Value: '+str(faceDetail['Mustache']['Value'])+'\n')
            self.DisplaySceneMarkInfo.insert(tk.END,'Pose : Pitch :'+str(faceDetail['Pose']['Pitch'])+' Roll :'+str(faceDetail['Pose']['Roll']) + ' Yaw :'+str(faceDetail['Pose']['Yaw'])+'\n')
            self.DisplaySceneMarkInfo.insert(tk.END,'Quality: Brightness :'+str(faceDetail['Quality']['Brightness']) +' Sharpness: '+str(faceDetail['Quality']['Sharpness'])+'\n')
            self.DisplaySceneMarkInfo.insert(tk.END,'Smile Confidence: '+str(faceDetail['Smile']['Confidence']) +' Value: '+str(faceDetail['Smile']['Value'])+'\n')
            self.DisplaySceneMarkInfo.insert(tk.END,'Sunglasses Confidence: '+str(faceDetail['Sunglasses']['Confidence']) +' Value: '+str(faceDetail['Sunglasses']['Value'])+'\n')
 
            for emotion in faceDetail['Emotions']:
                self.DisplaySceneMarkInfo.insert(tk.END,str(emotion['Type']) +' Confidence: '+str(emotion['Confidence'])+'\n')

        while True:
            # 複製一份原始影像
            #imOut = img.copy()
            # 顯示結果
            cv2.imshow("Output", imOut)
            # 讀取使用者所按下的鍵
            k = cv2.waitKey(0) & 0xFF
            # 若按下 q 鍵，則離開
            if k == 113:
                break
        # 關閉圖形顯示視窗
        cv2.destroyAllWindows()
    
    def celebrities(self, event = None):
        self.Name = ""
        client=boto3.client('rekognition')
        #self.imageFile = self.parent.imgswitch()
        #Call OpenCV Object img
        img = cv2.imread(self.imageFile)
        imOut = img
        #img of PIL object
        img_PIL = Image.open(self.imageFile)
        #width, height, channels = img.shape  #20190506 the size of OpenCV object is not good to use :(
        width, height = img_PIL.size
        #print(width, height, channels)
        with open(self.imageFile, 'rb') as image:
            celebrities_response = client.recognize_celebrities(Image={'Bytes': image.read()})
        cele_jsonfile = "celebritiesoutput.json"
        with open(cele_jsonfile, 'w') as fp:
            json.dump(celebrities_response, fp)
        

        for celebrity in celebrities_response['CelebrityFaces']:
            for eachperson in celebrity['Face']['Landmarks']:
                cv2.circle(imOut, (int(width*eachperson['X']), int(height*eachperson['Y'])), 1, self.color_1, -1)

            cv2.rectangle(imOut,
                          (int(width*celebrity['Face']['BoundingBox']['Left']),
                           int(height*celebrity['Face']['BoundingBox']['Top'])),
                          (int(width*(celebrity['Face']['BoundingBox']['Left']+celebrity['Face']['BoundingBox']['Width'])),
                           int(height*(celebrity['Face']['BoundingBox']['Top']+celebrity['Face']['BoundingBox']['Height']))),
                          self.color_2,int(self.linesizespinbox.get()))
            self.DisplaySceneMarkInfo.insert(tk.END,celebrity['Urls'])
            self.DisplaySceneMarkInfo.insert(tk.END,celebrity['Name'])
            self.Name = str(celebrity['Name'])
            self.DisplaySceneMarkInfo.insert(tk.END,"\n")
        self.open_webbrowser()

        while True:
            # 複製一份原始影像
            #imOut = img.copy()
            # 顯示結果
            cv2.imshow("Output", imOut)
            # 讀取使用者所按下的鍵
            k = cv2.waitKey(0) & 0xFF
            # 若按下 q 鍵，則離開
            if k == 113:
                break
        # 關閉圖形顯示視窗
        cv2.destroyAllWindows()
 
    def open_webbrowser(self):
        #import urllib.request
        import webbrowser
        from urllib.parse import quote
        #from urllib import quote
        #import webbrowser

        new = 2 # not really necessary, may be default on most modern browsers
        base_url = "http://www.google.com/?#q="
        #query = input("Please enter your search query: ")
        final_url = base_url + quote(self.Name)
        webbrowser.open(final_url, new=new)

    def label_rekognition(self, event = None):
        client=boto3.client('rekognition')
        #self.imageFile = self.parent.imgswitch()
        #Call OpenCV Object img
        img = cv2.imread(self.imageFile)
        imOut = img
        #img of PIL object
        img_PIL = Image.open(self.imageFile)
        #width, height, channels = img.shape  #20190506 the size of OpenCV object is not good to use :(
        width, height = img_PIL.size
        #print(width, height, channels)        
        with open(self.imageFile, 'rb') as image:
            label_response = client.detect_labels(Image={'Bytes': image.read()})
        label_jsonfile = "labeloutput.json"
        with open(label_jsonfile, 'w') as fp:
            json.dump(label_response, fp)
        print('Detected labels for ' + self.imageFile)

        for label in label_response['Labels']:
            self.DisplaySceneMarkInfo.insert(tk.END,label['Name'])
            self.DisplaySceneMarkInfo.insert(tk.END,"\n")
            for boundingbox in label['Instances']:
                #print(boundingbox)
                cv2.rectangle(imOut,
                              (int(width*boundingbox['BoundingBox']['Left']),int(height*boundingbox['BoundingBox']['Top'])),
                               (int(width*(boundingbox['BoundingBox']['Left']+boundingbox['BoundingBox']['Width'])),int(height*(boundingbox['BoundingBox']['Top']+boundingbox['BoundingBox']['Height']))),
                               self.color_1,
                               int(self.linesizespinbox.get()))
                cv2.putText(imOut, label['Name'],
                       (int(width*boundingbox['BoundingBox']['Left']),int(height*boundingbox['BoundingBox']['Top'])),
                        self.fontcv2Var.get(),
                        int(self.fontsizespinbox.get()),
                        self.color_2,
                        int(self.linesizespinbox.get()), 
                        self.fontlinetypecv2Var.get())

        while True:
            # 複製一份原始影像
            #imOut = img.copy()
            # 顯示結果
            cv2.imshow("Output", imOut)
            # 讀取使用者所按下的鍵
            k = cv2.waitKey(0) & 0xFF
            # 若按下 q 鍵，則離開
            if k == 113:
                break
        # 關閉圖形顯示視窗
        cv2.destroyAllWindows()

    def text_rekognition(self, event = None):
        client=boto3.client('rekognition')
        #self.imageFile = self.parent.imgswitch()
        #Call OpenCV Object img
        img = cv2.imread(self.imageFile)
        imOut = img
        #img of PIL object
        img_PIL = Image.open(self.imageFile)
        #width, height, channels = img.shape  #20190506 the size of OpenCV object is not good to use :(
        width, height = img_PIL.size
        #print(width, height, channels)
        with open(self.imageFile, 'rb') as image:
            text_response = client.detect_text(Image={'Bytes': image.read()})
            
        text_jsonfile = "textoutput.json"
        with open(text_jsonfile, 'w') as fp:
            json.dump(text_response, fp)

        #i = 0
        for text in text_response['TextDetections']:
            #Rectangle The text BoundingBox       
            cv2.rectangle(imOut,
            (int(width*text['Geometry']['BoundingBox']['Left']),
            int(height*text['Geometry']['BoundingBox']['Top'])),
            (int(width*(text['Geometry']['BoundingBox']['Left']+text['Geometry']['BoundingBox']['Width'])),
            int(height*(text['Geometry']['BoundingBox']['Top']+text['Geometry']['BoundingBox']['Height']))),
            self.color_1,
            int(self.linesizespinbox.get()))
            #1-2. print the text
            cv2.putText(imOut,
                        text['DetectedText'],
                        (int(width*text['Geometry']['BoundingBox']['Left']),int(height*text['Geometry']['BoundingBox']['Top'])),
                         self.fontcv2Var.get(), #int(self.fontcv2spinbox.get()),
                         int(self.fontsizespinbox.get()),
                         self.color_2,
                         int(self.linesizespinbox.get()), 
                         self.fontlinetypecv2Var.get())#int(self.fontlinetypecv2spinbox.get()))

            self.DisplaySceneMarkInfo.insert(tk.END,text['DetectedText']+'\n')

        while True:
            # 顯示結果
            cv2.imshow("Output", imOut)
            # 讀取使用者所按下的鍵
            k = cv2.waitKey(0) & 0xFF
            # 若按下 q 鍵，則離開
            if k == 113:
                break
        # 關閉圖形顯示視窗
        cv2.destroyAllWindows()

    def Compare_rekognition(self, event = None):
        sourceFile = self.imageFile1

        targetFile= self.imageFile2

        client=boto3.client('rekognition')
    
        img_PIL_2 = Image.open(sourceFile)
        img_2 = cv2.imread(sourceFile)
        #width_2, height_2, channels_2 = img_2.shape
        #print(width_2, height_2, channels_2)
        width_2, height_2 = img_PIL_2.size

        img_PIL_3 = Image.open(targetFile)
        img_3 = cv2.imread(targetFile)
        #width_3, height_3, channels_3 = img_3.shape
        #print(width_3, height_3, channels_3)
        width_3, height_3 = img_PIL_3.size
   
        '''collecting message from image'''
        image_from_source = np.zeros((600, 900, 3), np.uint8)
        image_from_source.fill(10)
        image_from_target = np.zeros((600, 900, 3), np.uint8)
        image_from_target.fill(10)
           
        '''Compare two pictures'''
        imageSource=open(sourceFile,'rb')
        imageTarget=open(targetFile,'rb')

        compare_response=client.compare_faces(SimilarityThreshold=70,
                                              SourceImage={'Bytes': imageSource.read()},
                                              TargetImage={'Bytes': imageTarget.read()})
        """
        print("===================================================================\n")
        print("Compare two pictures\n")
        print("===================================================================\n")
        for faceMatch in compare_response['FaceMatches']:
            position = faceMatch['Face']['BoundingBox']
            similarity = str(faceMatch['Similarity'])
            print('The face at ' +
                   str(position['Left']) + ' ' +
                   str(position['Top']) +
                   ' matches with ' + similarity + '% confidence')
        print('++++++++++++++++++++++++++++++++')
        print('Here are the other attributes:')
        print('++++++++++++++++++++++++++++++++')
        print(json.dumps(compare_response, indent=4, sort_keys=True))
        """

        imageSource.close()
        imageTarget.close()

        while True:

            imOut_2 = img_2.copy()
            imOut_3 = img_3.copy()
                
            #Rectangle the Source face BoundingBox
            source_left = int(width_2*compare_response['SourceImageFace']['BoundingBox']['Left'])
            source_right = int(width_2*(compare_response['SourceImageFace']['BoundingBox']['Left']+compare_response['SourceImageFace']['BoundingBox']['Width']))
            source_top = int(height_2*compare_response['SourceImageFace']['BoundingBox']['Top'])
            source_bottom = int(height_2*(compare_response['SourceImageFace']['BoundingBox']['Top']+compare_response['SourceImageFace']['BoundingBox']['Height']))
            cv2.rectangle(imOut_2,
            (int(width_2*compare_response['SourceImageFace']['BoundingBox']['Left']),
             int(height_2*compare_response['SourceImageFace']['BoundingBox']['Top'])),
            (int(width_2*(compare_response['SourceImageFace']['BoundingBox']['Left']+compare_response['SourceImageFace']['BoundingBox']['Width'])),
             int(height_2*(compare_response['SourceImageFace']['BoundingBox']['Top']+compare_response['SourceImageFace']['BoundingBox']['Height']))),
            self.color_1,int(self.linesizespinbox.get()))
            #copy and paste the source image
            source_roi = imOut_2[source_top:source_bottom, source_left:source_right]
            image_from_source[0:source_bottom-source_top, 0:source_right-source_left] = source_roi

            #Rectangle the Target faces BoundingBox
            target_left = int(width_3*compare_response['FaceMatches'][0]['Face']['BoundingBox']['Left'])
            target_right = int(width_3*(compare_response['FaceMatches'][0]['Face']['BoundingBox']['Left']+compare_response['FaceMatches'][0]['Face']['BoundingBox']['Width']))
            target_top = int(height_3*compare_response['FaceMatches'][0]['Face']['BoundingBox']['Top'])
            target_bottom = int(height_3*(compare_response['FaceMatches'][0]['Face']['BoundingBox']['Top']+compare_response['FaceMatches'][0]['Face']['BoundingBox']['Height']))
            cv2.rectangle(imOut_3,
            (int(width_3*compare_response['FaceMatches'][0]['Face']['BoundingBox']['Left']),
             int(height_3*compare_response['FaceMatches'][0]['Face']['BoundingBox']['Top'])),
            (int(width_3*(compare_response['FaceMatches'][0]['Face']['BoundingBox']['Left']+compare_response['FaceMatches'][0]['Face']['BoundingBox']['Width'])),
             int(height_3*(compare_response['FaceMatches'][0]['Face']['BoundingBox']['Top']+compare_response['FaceMatches'][0]['Face']['BoundingBox']['Height']))),
            self.color_1,int(self.linesizespinbox.get()))
            #copy and paste the target image
            target_roi = imOut_3[target_top:target_bottom, target_left:target_right]
            image_from_target[0:target_bottom-target_top, 0:target_right-target_left] = target_roi

        
            #Circle The Target face Landmarks
            for faceDetail in compare_response['FaceMatches'][0]['Face']['Landmarks']:
                cv2.circle(imOut_3, (int(width_3*faceDetail['X']), int(height_3*faceDetail['Y'])), int(self.linesizespinbox.get()), self.color_2, -1)

            #Rectangle the unmatched faces BoundingBox
            for unmatchedfaces in compare_response['UnmatchedFaces']:
                cv2.rectangle(imOut_3,
                (int(width_3*unmatchedfaces['BoundingBox']['Left']),
                 int(height_3*unmatchedfaces['BoundingBox']['Top'])),
                (int(width_3*(unmatchedfaces['BoundingBox']['Left']+unmatchedfaces['BoundingBox']['Width'])),
                 int(height_3*(unmatchedfaces['BoundingBox']['Top']+unmatchedfaces['BoundingBox']['Height']))),
                self.color_2,int(self.linesizespinbox.get()))
                #Circle the unmatched faces Landmarks
                for faceDetail in unmatchedfaces['Landmarks']:
                    cv2.circle(imOut_3, (int(width_3*faceDetail['X']), int(height_3*faceDetail['Y'])), int(self.linesizespinbox.get()), self.color_2, -1)
        
            # Show the result
            cv2.imshow("Output_2", imOut_2)
            cv2.imshow("Output_3", imOut_3)
        
            # show the message on another 
            cv2.imshow("image_from_source", image_from_source)
            cv2.imshow("image_from_target", image_from_target)

            k = cv2.waitKey(0) & 0xFF

            if k == 109:
                numShowRects += increment

            elif k == 108 and numShowRects > increment:
                numShowRects -= increment

            elif k == 113:
                break

        cv2.destroyAllWindows()

        print('Done...')
    def load_picture(self, event = None):
        self.localpicturename.set(filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("jpg files","*.[jJ][pP][gG]"),("all files","*.*"))))
        #self.LOCAL_VIDEO_NAME.set(self.localpicturename)
if __name__ == '__main__':
    root = tk.Tk()
    awsrekognition(root)
    #root.resizable(width=True, height=True)
    #root.geometry(MAIN_DISPLAY_SIZE)
    root.mainloop()
