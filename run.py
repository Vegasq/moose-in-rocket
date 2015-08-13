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

import random

import resources


class Block(Widget):
    x = NumericProperty(0)
    y = NumericProperty(Window.height)

    drop_speed = 5
    active = True

    def __init__(self, **kwargs):
        super(Block, self).__init__(**kwargs)
        # self.y = Window.width

        with self.canvas:
            Color(1, 0, 0, 1)  # set the colour to red
            self.image = Image(
                source=resources.asteroid['sprite'],
                pos=(self.x, self.height))
        self.image.size = self.image.texture.size
        self.size = self.image.size

    @classmethod
    def build(cls):
        return cls()

    def move(self):
        if self.active:
            self.y -= self.drop_speed
            self._move()
        self.image.pos = (self.x, self.y)
        self.pos = self.image.pos

    def _move(self):
        raise Exception('Implement _move')

    def _fix_collider(self):
        raise Exception('Implement _fix_collider')


class ShakeBlock(Block):
    shake_step = 5

    def _move(self):
        if self.x > Window.width / 2 - self.size[0] / 2 or\
           self.x < self.size[0] / 2 * -1:
            self.shake_step *= -1
        self.x += self.shake_step

        if self.y < self.image.size[1] * -1:
            self.active = False


class CrossBlock(Block):
    shake_step = 5

    def _move(self):
        self.x += self.shake_step

        if self.y < self.image.size[1] * -1 or self.x >= Window.height:
            self.active = False


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

    def move(self, speed):
        if (self.image.pos[1] * -1) >= self.resource['height']:
            self.image.pos = (self.image.pos[0],
                              self.resource['height'])
        self.image.pos = (self.image.pos[0], self.image.pos[1] - speed)


class BackgroundHandler(object):
    def __init__(self):
        self.level1A = Background(resource=resources.background1,
                                  pos=(0, 0))
        self.level1B = Background(resource=resources.background1,
                                  pos=(0, resources.background1['height']))

        self.level2A = Background(resource=resources.background2,
                                  pos=(0, 0))
        self.level2B = Background(resource=resources.background2,
                                  pos=(0, resources.background2['height']))

        self.level3A = Background(resource=resources.background3,
                                  pos=(0, 0))
        self.level3B = Background(resource=resources.background3,
                                  pos=(0, resources.background3['height']))

    def move(self):
        self.level1A.move(speed=10)
        self.level1B.move(speed=10)
        self.level2A.move(speed=7)
        self.level2B.move(speed=7)
        self.level3A.move(speed=5)
        self.level3B.move(speed=5)


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
    default_y = 120
    y = NumericProperty(120)
    x = NumericProperty(Window.width/2)
    force = BooleanProperty(False)
    dead = False

    def __init__(self, **kwargs):
        super(Rocket, self).__init__(**kwargs)
        self.x = Window.width/2 - self.size[0]/2

        with self.canvas:
            self.image = Image(pos=(self.x, self.y),
                               source=resources.rocket['sprite2'],)
            self.image.size = (resources.rocket['width'],
                               resources.rocket['height'])
        self.size = self.image.size
        self.pos = self.image.pos

        self.matrix = Matrix()

    def move(self):
        if self.dead:
            if self.image.pos[0] > resources.rocket['width'] * -1 and\
                    self.image.pos[1] > resources.rocket['height'] * -1:
                self.image.pos = (self.image.pos[0] - 20,
                                  self.image.pos[1] - 20)
                self.image.size = (self.image.size[0] - 25,
                                   self.image.size[1] - 10)
            return

        print('Rocket:')
        print(self.pos)
        print(self.image.pos)
        print(self.size)
        print(self.image.size)

        if self.force:
            self.image.source = resources.rocket['sprite1']
            self.image.reload()
            # if self.image.pos[1] < (Window.height - self.default_y - 150):
            #     self.die()
            self.image.pos = (self.image.pos[0], self.image.pos[1] + 10)
            self.pos = (self.image.pos[0], self.image.pos[1] + 10)
        else:
            self.image.source = resources.rocket['sprite2']
            self.image.reload()

            self.image.pos = (self.image.pos[0], self.image.pos[1] - 10)
            self.pos = (self.image.pos[0], self.image.pos[1] - 10)

            if self.image.pos[1] < 0 or\
                self.image.pos[1] > Window.height + self.image.size[1]:
                self.die()
                # self.image.pos = (self.image.pos[0], self.default_y)
                # self.pos = (self.image.pos[0], self.default_y)

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
        self.y -= 10
        self.image.pos = (self.x, self.y)


class MooseInRocketGame(Widget):
    rocket = ObjectProperty(None)
    background_handler = ObjectProperty(None)
    game_started = False

    def __init__(self, **kwargs):
        super(MooseInRocketGame, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self._keyboard.bind(on_key_up=self._on_keyboard_up)

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
                print('die')
            else:
                print('~')

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if not self.game_started:
            self.game_started = True
        self.rocket.force = True

    def _on_keyboard_up(self, keyboard, keycode):
        self.rocket.force = False


class MooseInRocketApp(App):
    def build(self):

        # Window.size = (1024, 768)
        #
        # def resize(w, h):
        #     if w == 768 and h == 1024:
        #         return
        #     Window.size = (768, 1024)
        #
        # Window.on_resize = resize

        game = MooseInRocketGame()

        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game

if __name__ == '__main__':
    MooseInRocketApp().run()
