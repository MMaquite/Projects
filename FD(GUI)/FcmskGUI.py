import cv2
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivy.clock import Clock
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget

#Use load_string if you dont want to creat new kivy file just add 3 ' to the () just like this (''' ''')
#To load the file Test.kv
Builder.load_file('Test.kv')


class MainScreen(Widget):
    def build(self):
        pass

class MyCameraApp(App):
    def build(self):
        return MainScreen()

class CameraPreview(Image):
    def __init__(self, **kwargs):
        super(CameraPreview, self).__init__(**kwargs)
        #Connect to 0th camera
        self.capture = cv2.VideoCapture(0)
        #Set drawing interval
        Clock.schedule_interval(self.update, 1.0 / 30)

    #Drawing method to execute at intervals
    def update(self, dt):
        #Load frame
        ret, self.frame = self.capture.read()
        #Convert to Kivy Texture
        buf = cv2.flip(self.frame, 0).tostring()

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

# Shoot button
class ImageButton(ButtonBehavior, Image):
    preview = ObjectProperty(None)

        # Execute when the button is pressed
    def on_press(self):
        cv2.namedWindow("CV2 Image")
        cv2.imshow("CV2 Image", self.preview.frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == '__main__':
    MyCameraApp().run()