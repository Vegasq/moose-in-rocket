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

import resources


class Block(Widget):
    y = NumericProperty(Window.height)
    x1 = NumericProperty((Window.width/2)*-1 - 200)
    # x2 = NumericProperty((Window.width/2)+200)
    shake_step = 5
    drop_speed = 5

    def __init__(self, **kwargs):
        super(Block, self).__init__(**kwargs)
        # self.y = Window.width

        with self.canvas:
            Color(1, 0, 0, 1)  # set the colour to red
            self.image = Rectangle(pos=(self.x1, self.height),
                                   size=(Window.width,
                                        100))
            # Color(1, 0, 0, 1)  # set the colour to red
            # self.rectB = Rectangle(pos=(self.x2, self.height),
            #                        size=(Window.width,
            #                             100))
        self.size = (Window.width, 100)

    def shake(self):
        if self.x1 > Window.width/2*-1 or self.x1 < (Window.width/3*2*-1):
            self.shake_step *= -1
            # if self.shake_step > 0:
            #     self.shake_step += 2
            # self.drop_speed += 1

        self.x1 += self.shake_step
        # self.x2 += self.shake_step

    def move(self):
        print('Block:')
        print(self.pos)
        print(self.image.pos)
        print(self.size)
        print(self.image.size)

        self.y -= self.drop_speed
        self.shake()
        self.image.pos = (self.x1, self.y)
        self.pos = self.image.pos
        # self.rectB.pos = (self.x2, self.y)

        if self.y < -100:
            self.y = Window.height + 100


class Background(Widget):
    y = NumericProperty(0)
    x = NumericProperty(0)

    def __init__(self, **kwargs):
        super(Background, self).__init__(**kwargs)
        self._requested_size = kwargs['size']

        with self.canvas:
            self.image = Rectangle(pos=kwargs['pos'],
                                   size=kwargs['size'],
                                   source=resources.background)

    def move(self):
        if (self.image.pos[1] * -1) >= self._requested_size[1]:
            self.image.pos = (self.image.pos[0], 1024*2)
        self.image.pos = (self.image.pos[0], self.image.pos[1] - 8)


class Enemies(object):
    _enemies = []

    @property
    def enemies(self):
        return self._enemies

    @enemies.setter
    def enemies(self, value):
        if value not in self._enemies:
            self._enemies.append(value)

    def generate(self):
        if self.enemies:
            return None
        block = Block()
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
            self.image = Rectangle(pos=(self.x, self.y),
                                   source=resources.rocket,)
            self.image.size = self.image.texture.size
        self.size = self.image.size
        self.pos = self.image.pos

    def move(self):
        if self.dead:
            return

        print('Rocket:')
        print(self.pos)
        print(self.image.pos)
        print(self.size)
        print(self.image.size)

        if self.force:
            # if self.image.pos[1] < (Window.height - self.default_y - 150):
            #     self.die()
            self.image.pos = (self.image.pos[0], self.image.pos[1] + 10)
            self.pos = (self.image.pos[0], self.image.pos[1] + 10)
        else:
            self.image.pos = (self.image.pos[0], self.image.pos[1] - 10)
            self.pos = (self.image.pos[0], self.image.pos[1] - 10)

            if self.image.pos[1] < 0 or\
                self.image.pos[1] > Window.height + self.image.size[1]:
                self.die()
                # self.image.pos = (self.image.pos[0], self.default_y)
                # self.pos = (self.image.pos[0], self.default_y)

    def die(self):
        self.dead = True
        print(dir(self.image))
        self.image.source = None


class StartPlace(Widget):
    y = NumericProperty(0)
    x = NumericProperty(0)

    def __init__(self, **kwargs):
        super(StartPlace, self).__init__(**kwargs)
        with self.canvas:
            self.image = Rectangle(pos=(self.x, self.y),
                                   source=resources.rocket)

    def move(self):
        self.y -= 10
        self.image.pos = (self.x, self.y)


class MooseInRocketGame(Widget):
    rocket = ObjectProperty(None)
    backgroundA = ObjectProperty(None)
    backgroundB = ObjectProperty(None)
    game_started = False

    def __init__(self, **kwargs):
        super(MooseInRocketGame, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self._keyboard.bind(on_key_up=self._on_keyboard_up)

        # self.rocket = Rocket()
        self.enemies_factory = Enemies()
        with self.canvas:
            self.backgroundA = Background(size=(768*2, 1024*2,), pos=(0, 0))
            self.backgroundB = Background(size=(768*2, 1024*2,), pos=(0, 1024*2))
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

        self.backgroundA.move()
        self.backgroundB.move()
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
