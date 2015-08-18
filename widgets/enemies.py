from kivy.uix.widget import Widget
from kivy.properties import NumericProperty
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle
from kivy.metrics import  dp, sp

from utils.sizer import Sizer
import resources

__author__ = 'vegasq'


class Collide(Widget):
    debug = True
    def __init__(self, **kwargs):
        super(Collide, self).__init__(**kwargs)
        self.remove_width = dp(280)
        self.remove_height = dp(120)
        if self.debug:
            with self.canvas:
                Color(1, 0, 0)
                self.rect = Rectangle()

    def setup(self, remove_width=10, remove_height=10):
        self.remove_width = dp(remove_width)
        self.remove_height = dp(remove_height)

    def follow(self, obj):
        self.size = (obj.size[0] - self.remove_width,
                     obj.size[1] - self.remove_height)

        self.pos = (obj.pos[0] + self.remove_width/2,
                    obj.pos[1] + self.remove_height/2)
        if self.debug:
            self.rect.size = self.size
            self.rect.pos = self.pos


class Block(Widget):
    x = NumericProperty(0)
    y = NumericProperty(Window.height)

    drop_speed = 10
    active = True

    collide = None

    def __init__(self, **kwargs):
        super(Block, self).__init__(**kwargs)

        with self.canvas:
            self.image = Image(
                source=self.sprite['sprite'],
                pos=(self.x, self.y),
                size=(self.sprite['width'],
                      self.sprite['height']))
        self.collide = Collide()

    def reset(self):
        self.active = False
        self.image.pos = (Window.width * -1, Window.height * -1)
        self.pos = self.image.pos

    @classmethod
    def build(cls):
        return cls()

    def move(self):
        if self.active:
            self.y -= self.drop_speed
            self._move()
        self.image.pos = (self.x, self.y)
        # self.rect.pos = (self.x, self.y)
        self.pos = self.image.pos
        self.collide.follow(self.image)

    def _move(self):
        raise Exception('Implement _move')

    def _fix_collider(self):
        raise Exception('Implement _fix_collider')


class ShakeBlock(Block):
    shake_step = 15
    sprite = resources.asteroid

    def _move(self):
        if self.x > self.image.size[0] or self.x < self.image.size[0] * -1:
            self.shake_step *= -1
        self.x += self.shake_step

        if self.y < self.image.size[1] * -1:
            self.active = False


class CrossBlock(Block):
    shake_step = 15
    sprite = resources.asteroid

    def _move(self):
        self.x += self.shake_step

        if self.y < self.image.size[1] * -1 or\
            self.x >= Window.width + self.image.size[0]:
            self.active = False


class CrossRoundBlock(Block):
    sprite = resources.asteroid_round
    shake_step = 10

    def __init__(self, **kwargs):
        super(CrossRoundBlock, self).__init__(**kwargs)
        self.collide.setup(90, 90)

    def _move(self):
        self.x += self.shake_step

        if self.x >= Window.height + self.image.size[0]:
            self.active = False
