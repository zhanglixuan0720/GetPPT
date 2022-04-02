import tkinter
from time import sleep
# from PIL import ImageGrab
from pyautogui import screenshot
import ctypes
import _thread
import numpy as np

FileName = 'test'
Rate = 1
ResRate =0.03

sleepTime = 1/Rate

class GetPPT:
    def __init__(self):
        self.pptk = tkinter.Tk()
        self.shotB = tkinter.Button(self.pptk, text ="screenshot", command = self.shotCallBack)
        self.startB= tkinter.Button(self.pptk, text ="start", command = self.startCallBack)
        self.endB= tkinter.Button(self.pptk, text ="end", command = self.endCallBack)
        
        self.pptk.bind('<Escape>', lambda e: self.pptk.destroy())
        

        user32 = ctypes.windll.user32
        gdi32 = ctypes.windll.gdi32
        dc = user32.GetDC(None)
        self.widthScale = gdi32.GetDeviceCaps(dc, 8)  
        # heightScale = gdi32.GetDeviceCaps(dc, 10)  
        self.width = gdi32.GetDeviceCaps(dc, 118) 
        # self.__start_x, self.__start_y = 0, 0
        self.__scale = self.width / self.widthScale

        self.shot=False
        self.__start_x, self.__start_y= -1,-1
        self.start=False
        self.iter=0
        self.isDetect =False
        self.screenPoint=None

        self.shotB.pack()
        self.startB.pack()
        self.endB.pack()
        self.pptk.mainloop()

    def shotCallBack(self):
        self.draw = tkinter.Tk()
        self.draw.bind('<Button-1>', self.buttonCallBack)  
        self.draw.bind('<ButtonRelease-1>', self.buttonCallBack)  
        self.draw.bind('<B1-Motion>', self.buttonRightCallBack)  
        self.draw.bind('<Escape>', lambda e: self.draw.destroy())

        self.draw.attributes("-alpha", 0.5)  
        self.draw.attributes("-fullscreen", True)


        self.draw_width, self.draw_height = self.draw.winfo_screenwidth(), self.draw.winfo_screenheight()

        # 创建画布
        self.__canvas = tkinter.Canvas(self.draw, width=self.draw_width, height=self.draw_height, bg="gray")
        # height = gdi32.GetDeviceCaps(dc, 117) 
        
        self.shot=True
        print("hello callback!")
        # tkMessageBox.showinfo( "Hello Python", "Hello Runoob")
    def startCallBack(self):
        if self.screenPoint is None:
            return
        while self.isDetect:
            self.start=False
        self.start=True
        _thread.start_new_thread(self.detect,())
        print(self.screenPoint)

    def endCallBack(self):
        self.start=False
        print("end!")

    def buttonCallBack(self,event):
        if self.shot==True:
            print(event.state)
            if event.state == 8:  # 鼠标左键按下
                self.__start_x, self.__start_y = event.x, event.y
            elif event.state == 264:  # 鼠标左键释放
                if self.__start_x<0:
                    return 
                if event.x == self.__start_x or event.y == self.__start_y:
                    return
                point4= (self.__scale * self.__start_x, self.__scale * self.__start_y,
                                    self.__scale * event.x, self.__scale * event.y)
                self.screenPoint =(point4[0],point4[1],point4[2]-point4[0],point4[3]-point4[1])
                # im = ImageGrab.grab(self.screen_point)
                # imgName = 'tmp.png'
                # # print('保存成功')
                # im.save(imgName)
                self.shot=False
                self.__start_x, self.__start_y= -1,-1
                # self.__canvas.delete("all")
                # print('保存成功')
                self.draw.update()
                sleep(0.5)
                self.draw.destroy()
            # print("OK",event)
    def buttonRightCallBack(self, event):
        if self.__start_x <0:
            return
        if event.x == self.__start_x or event.y == self.__start_y:
            return
        self.__canvas.delete("prscrn")
        self.__canvas.create_rectangle(self.__start_x, self.__start_y, event.x, event.y,
                                       fill='white', outline='red', tag="prscrn")
        # 包装画布
        self.__canvas.pack()

    def detect(self):
        self.isDetect =True
        img_l = np.array(screenshot(region=self.screenPoint))
        maxPixels=img_l.shape[0]*img_l.shape[1]*255
        while self.start:
            # if self.start == False:
            #     break
            # im = ImageGrab.grab(self.point_screen)
            # img = np.array(im)
            # if img_l is None:
            #     img_l = img
            #     imgName = FileName+str(self.iter)+'.png'
            #     self.iter += 1
            #     im.save(imgName)
            # else:
            # im = ImageGrab.grab(self.screenPoint)
            im =screenshot(region=self.screenPoint)
            img = np.array(im)
            print("comapre")
            if np.abs(img-img_l).sum() > maxPixels*ResRate:
                imgName = FileName+str(self.iter)+'.png'
                self.iter += 1
                im.save(imgName)
            img_l = img
            sleep(sleepTime)
        self.isDetect =False
                

if __name__ == '__main__':
    GetPPT()
