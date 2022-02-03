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

# modules
import os

# import our face mask detector
import detect_mask_video

# globals
isRunning = False

Builder.load_file("Menu.kv")

class Widgetfacemask(RelativeLayout):
    # RelativeLayout
    perspective_point_x =NumericProperty(0)
    perspective_point_x =NumericProperty(0)

    # buttons
    button_start = True
 
    def __init__(self, **kw):
        super(Widgetfacemask,self).__init__(**kw)
        
    def on_size (self,*args):
        print("ON SIZE W:"+str(self.width)+"H"+str(self.height))
    
    def on_perspective_point_x(self,widget,value):
        print("PX:"+str(value))

    def on_perspective_point_y(self,widget,value):
        print("PY:"+str(value))
    
    # button start
    def button_start(self, widget):
        global isRunning
        
        if widget.state != "normal":
            isRunning = True
            widget.text = "Stop"
            # disable all buttons
            self.ids.button_train.disabled = True
            self.ids.button_option.disabled = True
            self.ids.button_exit.disabled = True
        else:
            isRunning = False
            widget.text = "Start"
            # enable all buttons
            self.ids.button_train.disabled = False
            self.ids.button_option.disabled = False
            self.ids.button_exit.disabled = False

        print("IsRunning:"+widget.state)

    def button_train(self,widget):
        print("Train Face Mask Detector")
        os.system('start cmd /k "python ./train_mask_detector.py"')

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
        Clock.schedule_interval(self.update, 1.0 / 30)

    #Drawing method to execute at intervals
    def update(self, dt):
        global isRunning
        if isRunning == True:

            # fix disable image on screen
            self.opacity = 1

            #Load frame
            frame = self.capture.read()

            #Proccess our frame in startVideoFeed
            self.frame = detect_mask_video.startVideoFeed(frame)

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