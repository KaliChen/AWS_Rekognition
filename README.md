# AWS_Rekognition

## Face Rekognition
![https://ithelp.ithome.com.tw/upload/images/20201001/20119608fT70fF22Sw.jpg](https://ithelp.ithome.com.tw/upload/images/20201001/20119608fT70fF22Sw.jpg)
```
    def face_rekognition(self,event = None):
        client=boto3.client('rekognition')
        img = cv2.imread(self.imageFile)
        img_PIL = Image.open(self.imageFile)
        width, height = img_PIL.size
        with open(self.imageFile, 'rb') as image:
            faces_response = client.detect_faces(Image=
                                                 {'Bytes': image.read()},
                                                           Attributes=['ALL'])
        face_jsonfile = "faceoutput.json"
        with open(face_jsonfile, 'w') as fp:
            json.dump(faces_response, fp)
        imOut = img.copy()
        for faceDetail in faces_response['FaceDetails']:
            cv2.rectangle(imOut,
                              (int(width*faceDetail['BoundingBox']['Left']),
                               int(height*faceDetail['BoundingBox']['Top'])),
                               (int(width*(faceDetail['BoundingBox']['Left']+
                                faceDetail['BoundingBox']['Width'])),
                               int(height*(faceDetail['BoundingBox']['Top']+
                               faceDetail['BoundingBox']['Height']))),
                              self.color_1,int(self.linesizespinbox.get()))
            for eachperson in faceDetail['Landmarks']:
                cv2.circle(imOut, 
                           (int(width*eachperson['X']), 
                            int(height*eachperson['Y'])),
                            int(self.linesizespinbox.get()),
                            self.color_2, 
                            -1)

        while True:
            cv2.imshow("Output", imOut)
            k = cv2.waitKey(0) & 0xFF
            if k == 113:
                break
        cv2.destroyAllWindows()
 ```
 ## Celebrities Rekognition
 偵測知名人士
![https://ithelp.ithome.com.tw/upload/images/20201002/20119608Ga1TqW7KQD.jpg](https://ithelp.ithome.com.tw/upload/images/20201002/20119608Ga1TqW7KQD.jpg)

    def celebrities(self, event = None):
        self.Name = ""
        client=boto3.client('rekognition')
        img = cv2.imread(self.imageFile)
        imOut = img
        img_PIL = Image.open(self.imageFile)
        width, height = img_PIL.size
        with open(self.imageFile, 'rb') as image:
            celebrities_response = client.recognize_celebrities(
                                           Image=
                                           {'Bytes': image.read()})
        cele_jsonfile = "celebritiesoutput.json"
        with open(cele_jsonfile, 'w') as fp:
            json.dump(celebrities_response, fp)
        for celebrity in celebrities_response['CelebrityFaces']:
            for eachperson in celebrity['Face']['Landmarks']:
                cv2.circle(imOut,
                           (int(width*eachperson['X']),
                            int(height*eachperson['Y'])),
                            1, self.color_1, -1)
            cv2.rectangle(imOut,
                          (int(width*celebrity['Face']['BoundingBox']['Left']),
                           int(height*celebrity['Face']['BoundingBox']['Top'])),
                          (int(width*(celebrity['Face']['BoundingBox']['Left']+
                           celebrity['Face']['BoundingBox']['Width'])),
                          int(height*(celebrity['Face']['BoundingBox']['Top']+
                           celebrity['Face']['BoundingBox']['Height']))),
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

打開瀏覽器搜尋

    def open_webbrowser(self):
        import webbrowser
        from urllib.parse import quote
        new = 2 # not really necessary, may be default on most modern browsers
        base_url = "http://www.google.com/?#q="
        #query = input("Please enter your search query: ")
        final_url = base_url + quote(self.Name)
        webbrowser.open(final_url, new=new)
        
![https://ithelp.ithome.com.tw/upload/images/20201002/20119608Lbyl3t525R.jpg](https://ithelp.ithome.com.tw/upload/images/20201002/20119608Lbyl3t525R.jpg)

## Label Rekognition
![https://ithelp.ithome.com.tw/upload/images/20201003/20119608ZeQLxC1YpK.jpg](https://ithelp.ithome.com.tw/upload/images/20201003/20119608ZeQLxC1YpK.jpg)
```
    def label_rekognition(self, event = None):
        client=boto3.client('rekognition')
        img = cv2.imread(self.imageFile)
        imOut = img
        img_PIL = Image.open(self.imageFile)
        width, height = img_PIL.size        
        with open(self.imageFile, 'rb') as image:
            label_response = client.detect_labels(
                                Image={'Bytes': image.read()})
        label_jsonfile = "labeloutput.json"
        with open(label_jsonfile, 'w') as fp:
            json.dump(label_response, fp)
        for label in label_response['Labels']:
            for boundingbox in label['Instances']:
                cv2.rectangle(imOut,
                              (int(width*boundingbox['BoundingBox']['Left']),
                               int(height*boundingbox['BoundingBox']['Top'])),
                              (int(width*(boundingbox['BoundingBox']['Left']+
                               boundingbox['BoundingBox']['Width'])),
                              int(height*(boundingbox['BoundingBox']['Top']+
                               boundingbox['BoundingBox']['Height']))),
                               self.color_1,
                               int(self.linesizespinbox.get()))
                cv2.putText(imOut,
                            label['Name'],  
                            (int(width*boundingbox['BoundingBox']['Left']),
                             int(height*boundingbox['BoundingBox']['Top'])),
                            self.fontcv2Var.get(),
                            int(self.fontsizespinbox.get()),
                            self.color_2,
                            int(self.linesizespinbox.get()), 
                            self.fontlinetypecv2Var.get())

        while True:
            cv2.imshow("Output", imOut)
            k = cv2.waitKey(0) & 0xFF
            # 若按下 q 鍵，則離開
            if k == 113:
                break
        cv2.destroyAllWindows()
```
## Text Rekognition
![https://ithelp.ithome.com.tw/upload/images/20201004/20119608Iy3ugvmXSR.jpg](https://ithelp.ithome.com.tw/upload/images/20201004/20119608Iy3ugvmXSR.jpg)
```
    def text_rekognition(self, event = None):
        client=boto3.client('rekognition')
        img = cv2.imread(self.imageFile)
        imOut = img
        img_PIL = Image.open(self.imageFile)
        width, height = img_PIL.size
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
             (int(width*(text['Geometry']['BoundingBox']['Left']+
              text['Geometry']['BoundingBox']['Width'])),
             int(height*(text['Geometry']['BoundingBox']['Top']+
             text['Geometry']['BoundingBox']['Height']))),
             self.color_1,
            int(self.linesizespinbox.get()))
            #print the text
            cv2.putText(imOut,
                        text['DetectedText'],
                        (int(width*text['Geometry']['BoundingBox']['Left']),
                         int(height*text['Geometry']['BoundingBox']['Top'])),
                         self.fontcv2Var.get(),
                         int(self.fontsizespinbox.get()),
                         self.color_2,
                         int(self.linesizespinbox.get()), 
                         self.fontlinetypecv2Var.get())
            self.DisplaySceneMarkInfo.insert(tk.END,text['DetectedText']+'\n')

        while True:
            cv2.imshow("Output", imOut)
            k = cv2.waitKey(0) & 0xFF
            if k == 113:
                break
        cv2.destroyAllWindows()

```
