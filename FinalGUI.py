from tkinter import NUMERIC
from unicodedata import numeric
from cv2 import perspectiveTransform
import kivy
import cv2
from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import NumericProperty
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivy.clock import Clock
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget
from imutils.video import VideoStream
from kivy.config import Config

# modules
import os

# import our face mask detector
import detect_mask_video

# globals
isRunning = False
checker = False

Builder.load_file("Menu.kv")

class Widgetfacemask(RelativeLayout):
    # RelativeLayout
    perspective_point_x =NumericProperty(0)
    perspective_point_x =NumericProperty(0)

    # well use this to make our alert popup when checker is True and return the state if our alert is clicked.
    def update(self, dt):
        global checker
        if checker == True:
            self.ids.button_mask.opacity=1

    # buttons
    button_start = True
 
    def __init__(self, **kw):
        super(Widgetfacemask,self).__init__(**kw)
        Clock.schedule_interval(self.update, 1.0 / 30) # this will keep our update function running
        
    def on_size (self,*args):
        print("ON SIZE W:"+str(self.width)+"H"+str(self.height))
    
    def on_perspective_point_x(self,widget,value):
        print("PX:"+str(value))

    def on_perspective_point_y(self,widget,value):
        print("PY:"+str(value))
    
    # button alert
    def button_mask(self, widget):
        global checker
        self.ids.button_mask.opacity = 0
        checker = False
       
    
    # button start
    def button_start(self, widget):
        global isRunning
        global checker
        
        if widget.state != "normal":
            isRunning = True
            widget.text = "Stop"
            # disable all buttons
            self.ids.button_train.disabled = True
            #self.ids.button_option.disabled = True
            self.ids.button_exit.disabled = True
        else:
            isRunning = False
            widget.text = "Start"   
            self.ids.button_mask.opacity=0
            checker = False
            # enable all buttons
            self.ids.button_train.disabled = False
            #self.ids.button_option.disabled = False
            self.ids.button_exit.disabled = False

        print("IsRunning:"+widget.state)

    def button_train(self,widget):
        print("Train Face Mask Detector")
        #os.system('start cmd /k "python ./train_mask_detector.py"')

    # button_exit
    def button_exit(self,widget):
        cv2.destroyAllWindows()
        exit()

class FinalApp(App):
    def build(self):
        self.title = 'Face Mask Detector'
    pass

class CameraPreview(Image):
    def __init__(self, **kwargs):
        super(CameraPreview, self).__init__(**kwargs)
        #Connect to 0th camera
        #self.capture = cv2.VideoCapture(0)
        self.capture = VideoStream(src=0).start()
        #Set drawing interval
        Clock.schedule_interval(self.update, 1.0 / 60)

    #Drawing method to execute at intervals
    def update(self, dt):
        global isRunning
        global checker
        
        if isRunning == True and checker == False:

            # fix disable image on screen
            self.opacity = 1

            #Load frame
            frame = self.capture.read()

            # Proccess our frame in startVideoFeed
            self.frame, self._checker = detect_mask_video.startVideoFeed(frame,int(kivy.core.window.Window.width),int(kivy.core.window.Window.height))
            checker = self._checker

            # if self.checker is true raise an alert dialog 
              # codes goes here i think.
            # Print Label
            # print("DETECTED:"+label)

            #Convert our proccesed frame into Kivy Texture
            buf = cv2.flip(self.frame, 0).tobytes()

            texture = Texture.create(
                size=(self.frame.shape[1],
                self.frame.shape[0]),
                colorfmt='bgr'
            )

            texture.blit_buffer(
                buf,
                colorfmt='bgr',
                bufferfmt='ubyte'
            )

            #Change the texture of the instance
            self.texture = texture
            pass
        
        elif isRunning == False:
            # fix disable image on screen
            self.opacity = 0
            pass

if __name__ == "__main__":
    FinalApp().run()