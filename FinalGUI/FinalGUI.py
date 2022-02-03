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

Builder.load_file("Menu.kv")

class Widgetfacemask(RelativeLayout):
    perspective_point_x =NumericProperty(0)
    perspective_point_x =NumericProperty(0)
    
    def __init__(self, **kw):
        super(Widgetfacemask,self).__init__(**kw)
        
    def on_size (self,*args):
        print("ON SIZE W:"+str(self.width)+"H"+str(self.height))
    
    def on_perspective_point_x(self,widget,value):
        print("PX:"+str(value))

    def on_perspective_point_y(self,widget,value):
        print("PY:"+str(value))
class FinalApp(App):
    pass


FinalApp().run()