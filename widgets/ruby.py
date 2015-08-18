from kivy.uix.widget import Widget
from kivy.properties import NumericProperty
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle

import resources

__author__ = 'vegasq'


class Ruby(Widget):
    x = NumericProperty(Window.width/2)
    y = NumericProperty(Window.height)
    active = True

    def __init__(self, **kwargs):
        super(Ruby, self).__init__(**kwargs)

        with self.canvas:
            # Color(1,0,0)
            # self.rect = Rectangle(
            #     pos=(self.x, self.y),
            #     size = Sizer.get_asteroid_size())
            self.image = Image(
                source=resources.ruby['sprite'],
                pos=(self.x, self.y))
        self.size = self.image.size
        self.x = Window.width/2 - self.image.size[1]/2

    def hide(self):
        # self.active = False
        self.image.pos = (self.image.pos[0], Window.height + self.image.size[1])
        self.pos = self.image.pos

    @classmethod
    def build(cls):
        return cls()

    def move(self):
        if self.active:
            self.y -= 5
            self.image.pos = (self.x, self.y)
            self.pos = self.image.pos
