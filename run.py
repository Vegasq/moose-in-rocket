from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty, BooleanProperty
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.vector import Vector

from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import AsyncImage, Image
from kivy.config import Config
from  kivy.graphics.context_instructions import Rotate
from kivy.graphics.transformation import Matrix
from kivy.metrics import  dp, sp

import random

import resources
from widgets.enemies import ShakeBlock, CrossBlock
from utils.sizer import Sizer


class Background(Widget):
    y = NumericProperty(0)
    x = NumericProperty(0)

    def __init__(self, **kwargs):
        super(Background, self).__init__(**kwargs)
        self.resource = kwargs['resource']
        with self.canvas:
            self.image = Rectangle(pos=kwargs['pos'],
                                   size=(self.resource['width'],
                                         self.resource['height']),
                                   source=self.resource['sprite'])

    def move(self, speed, total_slides):
        if (self.image.pos[1] * -1) >= self.resource['height']:
            self.image.pos = (self.image.pos[0],
                              self.image.pos[1] + self.resource['height'] * total_slides)
        self.image.pos = (self.image.pos[0], self.image.pos[1] - speed)


class BackgroundHandler(object):
    def __init__(self):
        self.level3A = Background(resource=resources.background3,
                                  pos=(0, 0))
        self.level3B = Background(resource=resources.background3,
                                  pos=(0, resources.background3['height']))
        # self.level1C = Background(resource=resources.background1,
        #                           pos=(0, resources.background1['height'] * 2))

        self.level1A = Background(resource=resources.background1,
                                  pos=(0, 0))
        self.level1B = Background(resource=resources.background1,
                                  pos=(0, resources.background1['height']))
        self.level1C = Background(resource=resources.background1,
                                  pos=(0, resources.background1['height'] * 2))

        self.level2A = Background(resource=resources.background2,
                                  pos=(0, 0))
        self.level2B = Background(resource=resources.background2,
                                  pos=(0, resources.background2['height']))
        self.level2C = Background(resource=resources.background2,
                                  pos=(0, resources.background2['height'] * 2))

    def move(self):
        self.level3A.move(speed=Sizer.get_screen_speed(), total_slides=2)
        self.level3B.move(speed=Sizer.get_screen_speed(), total_slides=2)
        # self.level1C.move(speed=Sizer.get_screen_speed())

        #
        self.level1A.move(speed=Sizer.get_screen_speed() -2, total_slides=3)
        self.level1B.move(speed=Sizer.get_screen_speed() -2, total_slides=3)
        self.level1C.move(speed=Sizer.get_screen_speed() -2, total_slides=3)

        self.level2A.move(speed=Sizer.get_screen_speed() -4, total_slides=3)
        self.level2B.move(speed=Sizer.get_screen_speed() -4, total_slides=3)
        self.level2C.move(speed=Sizer.get_screen_speed() -4, total_slides=3)


class Enemies(object):
    _enemies = []
    enemies_classes = [ShakeBlock, CrossBlock]

    @property
    def enemies(self):
        return self._enemies

    @enemies.setter
    def enemies(self, value):
        if value not in self._enemies:
            self._enemies.append(value)

    def generate(self):
        for enemie in self.enemies:
            if enemie.active:
                return

        enemie_cls = random.choice(self.enemies_classes)
        block = enemie_cls()
        self.enemies = block
        return block


class Rocket(Widget):
    default_y = dp(10)
    y = NumericProperty(dp(10))
    x = NumericProperty(Window.width/2 - Sizer.get_rocket_size()[0]/2)
    force = BooleanProperty(False)
    dead = False

    def __init__(self, **kwargs):
        super(Rocket, self).__init__(**kwargs)
        self.x = Window.width/2 - Sizer.get_rocket_size()[0]/2
        size = (resources.rocket['width'], resources.rocket['height'])

        with self.canvas:
            # Color(1,0,0)
            # self.rect = Rectangle(
            #     pos=(self.x, self.y),
            #     size=size)

            self.image = Image(source=resources.rocket['sprite2'],
                               pos=(self.x, self.y),
                               size=size)

        self.size = size
        self.pos = (self.x, self.y)

    def move(self):
        if self.dead:
            if self.image.pos[0] > resources.rocket['width'] * -1 and\
                    self.image.pos[1] > resources.rocket['height'] * -1:
                self.image.pos = (self.image.pos[0] - dp(20),
                                  self.image.pos[1] - dp(20))
                self.image.size = (self.image.size[0] - dp(25),
                                   self.image.size[1] - dp(10))
            return

        if self.force:
            self.image.source = resources.rocket['sprite1']
            self.image.reload()
            # if self.image.pos[1] < (Window.height - self.default_y - 150):
            #     self.die()
            self.image.pos = (self.image.pos[0], self.image.pos[1] + Sizer.get_rocket_speed())
            self.pos = (self.image.pos[0], self.image.pos[1] + Sizer.get_rocket_speed())
        else:
            self.image.source = resources.rocket['sprite2']
            self.image.reload()

            self.image.pos = (self.image.pos[0], self.image.pos[1] - Sizer.get_rocket_speed())
            self.pos = (self.image.pos[0], self.image.pos[1] - Sizer.get_rocket_speed())

            if (
                self.image.pos[1] < 0 or
                self.image.pos[1] > Window.height + self.image.size[1]
            ):
                self.die()

    def die(self):
        self.dead = True


class StartPlace(Widget):
    y = NumericProperty(0)
    x = NumericProperty(0)

    def __init__(self, **kwargs):
        super(StartPlace, self).__init__(**kwargs)
        with self.canvas:
            self.image = Rectangle(pos=(self.x, self.y),
                                   source=resources.basement['sprite'],
                                   size=(resources.basement['width'],
                                         resources.basement['height']))

    def move(self):
        self.y -= Sizer.get_screen_speed()
        self.image.pos = (self.x, self.y)


class MooseInRocketGame(Widget):
    rocket = ObjectProperty(None)
    background_handler = ObjectProperty(None)
    game_started = False

    def __init__(self, **kwargs):
        super(MooseInRocketGame, self).__init__(**kwargs)

        # self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        # self._keyboard.bind(on_key_down=self._on_keyboard_down)
        # self._keyboard.bind(on_key_up=self._on_keyboard_up)

        # self.rocket = Rocket()
        self.enemies_factory = Enemies()
        with self.canvas:
            self.background_handler = BackgroundHandler()
            self.start_place = StartPlace()
            self.rocket = Rocket()

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def update(self, dt):
        if not self.game_started:
            return
        with self.canvas:
            self.enemies_factory.generate()

        self.background_handler.move()
        self.start_place.move()
        self.rocket.move()
        for enemie in self.enemies_factory.enemies:
            enemie.move()
            if self.rocket.collide_widget(enemie):
                self.rocket.die()

    def on_touch_down(self, *args, **kwargs):
        self._on_keyboard_down(1,2,3,4)

    def on_touch_up(self, *args, **kwargs):
        self._on_keyboard_up(1,2)

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if not self.game_started:
            self.game_started = True
        self.rocket.force = True

    def _on_keyboard_up(self, keyboard, keycode):
        self.rocket.force = False


class MooseInRocketApp(App):
    def build(self):

        # width = 768
        # height = 1024
        #
        # Window.size = (width, height)
        #
        # def resize(w, h):
        #     if w == width and h == height:
        #         return
        #     Window.size = (width, height)
        #
        # Window.on_resize = resize

        game = MooseInRocketGame()

        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game

if __name__ == '__main__':
    MooseInRocketApp().run()
