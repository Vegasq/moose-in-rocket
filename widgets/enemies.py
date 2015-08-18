from kivy.uix.widget import Widget
from kivy.properties import NumericProperty
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle


from utils.sizer import Sizer
import resources

__author__ = 'vegasq'


class Block(Widget):
    x = NumericProperty(0)
    y = NumericProperty(Window.height + Sizer.get_asteroid_size()[1])
    sprite = resources.asteroid['sprite']

    drop_speed = 10
    active = True

    def __init__(self, **kwargs):
        super(Block, self).__init__(**kwargs)

        with self.canvas:
            # Color(1,0,0)
            # self.rect = Rectangle(
            #     pos=(self.x, self.y),
            #     size = Sizer.get_asteroid_size())
            self.image = Image(
                source=self.sprite,
                pos=(self.x, self.y),
                size = Sizer.get_asteroid_size())
        self.size = Sizer.get_asteroid_size()

    def reset(self):
        self.active = False
        self.image.pos = (Window.width * -1, Window.heightr * -1)
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

    def _move(self):
        raise Exception('Implement _move')

    def _fix_collider(self):
        raise Exception('Implement _fix_collider')


class ShakeBlock(Block):
    shake_step = 15
    sprite = resources.asteroid['sprite']

    def _move(self):
        if self.x > Window.width / 2 - self.size[0] / 2 or\
           self.x < self.size[0] / 2 * -1:
            self.shake_step *= -1
        self.x += self.shake_step

        if self.y < self.image.size[1] * -1:
            self.active = False


class CrossBlock(Block):
    shake_step = 15
    sprite = resources.asteroid['sprite']

    def _move(self):
        self.x += self.shake_step

        if self.y < self.image.size[1] * -1 or\
            self.x >= Window.width + self.image.size[0]:
            self.active = False


class CrossRoundBlock(Block):
    sprite = resources.asteroid_round['sprite']
    shake_step = 10

    def _move(self):
        self.x += self.shake_step

        if self.y < self.image.size[1] * -1 or self.x >= Window.height:
            self.active = False
