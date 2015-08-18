from kivy.uix.widget import Widget
from kivy.properties import NumericProperty
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle

import resources

__author__ = 'vegasq'


class Score(Widget):
    x = NumericProperty(10)
    y = NumericProperty(10)
    score = NumericProperty(0)

    def __init__(self, **kwargs):
        super(Score, self).__init__(**kwargs)

        with self.canvas:
            # Color(1,0,0)
            # self.rect = Rectangle(
            #     pos=(self.x, self.y),
            #     size = Sizer.get_asteroid_size())
            self.image = Image(
                source=resources.score['sprite'],
                pos=(self.x, self.y),
                size=(resources.score['width'], resources.score['height'])
            )

            self.text = Label(text=str(self.score))
            self.image.size = map(lambda val: val + 1, self.image.size)

        self.image.y = Window.height - (self.image.size[1])
        self.text.pos = (self.image.pos[0] + 50, self.image.pos[1] + 25)

    def up(self):
        self.score += 1
        self.text.text = str(self.score)
