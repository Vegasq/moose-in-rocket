from kivy.uix.widget import Widget
from kivy.properties import NumericProperty
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle

import resources

__author__ = 'vegasq'


class StartScreen(Widget):
    x = NumericProperty(0)
    y = NumericProperty(0)
    active = True

    def __init__(self, **kwargs):
        super(StartScreen, self).__init__(**kwargs)

        with self.canvas:
            self.image = Image(
                source=resources.start_screen['sprite'],
                pos=(self.x, self.y),
                size=(resources.start_screen['width'],
                      resources.start_screen['height'])
                )
            self.x = Window.width / 2 - resources.start_screen['width'] / 2
            self.y = Window.height / 2 - resources.start_screen['height'] / 2
            self.image.pos = (self.x, self.y)

    def hide(self):
        self.image.pos = (self.image.pos[0], Window.height + self.image.size[1])
        self.pos = self.image.pos

    def is_active(self):
        return not self.image.pos[1] >= Window.height + self.image.size[1]

    @classmethod
    def build(cls):
        return cls()

    def move(self):
        pass


class ScoreScreen(Widget):
    x = NumericProperty(0)
    y = NumericProperty(0)
    active = True

    def __init__(self, **kwargs):
        super(ScoreScreen, self).__init__(**kwargs)

        with self.canvas:
            self.image = Image(
                source=resources.score_screen['sprite'],
                pos=(self.x, self.y),
                size=(resources.score_screen['width'],
                      resources.score_screen['height'])
                )
            self.hide()

    def show(self):
        self.x = Window.width / 2 - resources.score_screen['width'] / 2
        self.y = Window.height / 2 - resources.score_screen['height'] / 2
        self.image.pos = (self.x, self.y)

    def hide(self):
        self.image.pos = (self.image.pos[0], Window.height + self.image.size[1])
        self.pos = self.image.pos

    def is_active(self):
        return not self.image.pos[1] >= Window.height + self.image.size[1]

    @classmethod
    def build(cls):
        return cls()

    def move(self):
        pass
