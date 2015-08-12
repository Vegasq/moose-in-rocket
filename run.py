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


class Block(Widget):
    y = NumericProperty(Window.height)
    x1 = NumericProperty((Window.width/2)*-1)
    x2 = NumericProperty((Window.width/2)+200)
    shake_step = 5

    def __init__(self, **kwargs):
        super(Block, self).__init__(**kwargs)
        # self.y = Window.width

        with self.canvas:
            Color(1, 0, 0, 1)  # set the colour to red
            self.rectA = Rectangle(pos=(self.x1, self.height),
                                  size=(Window.width,
                                        100))
            Color(1, 0, 0, 1)  # set the colour to red
            self.rectB = Rectangle(pos=(self.x2, self.height),
                                  size=(Window.width,
                                        100))

    def shake(self):
        if self.x2 > (Window.width / 2 + 300) or self.x2 < (Window.width / 2 - 200):
            self.shake_step *= -1

        self.x1 += self.shake_step
        self.x2 += self.shake_step

    def move(self):
        self.y -= 5
        self.shake()
        self.rectA.pos = (self.x1, self.y)
        self.rectB.pos = (self.x2, self.y)

        if self.y < -100:
            self.y = Window.height + 100


class Background(Widget):
    default_y = 120
    y = NumericProperty(120)
    x = NumericProperty(120)
    force = BooleanProperty(False)

    def move(self):
        if (self.y * -1) >= self.height:
            self.y = self.height
        self.y -= 7


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
    x = NumericProperty(120)
    force = BooleanProperty(False)

    def move(self):
        if self.force:
            if self.y < (Window.height - self.default_y - 150):
                self.y += 10
        elif self.y > self.default_y:
            self.y -= 10
            if self.y < self.default_y:
                self.y = self.default_y


class RocketGame(Widget):
    rocket = ObjectProperty(None)
    backgroundA = ObjectProperty(None)
    backgroundB = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(RocketGame, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self._keyboard.bind(on_key_up=self._on_keyboard_up)

        self.enemies_factory = Enemies()

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def update(self, dt):
        with self.canvas:
            self.enemies_factory.generate()

        for enemie in self.enemies_factory.enemies:
            enemie.move()
        self.rocket.move()
        self.backgroundA.move()
        self.backgroundB.move()

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        self.rocket.force = True

    def _on_keyboard_up(self, keyboard, keycode):
        self.rocket.force = False


class RocketApp(App):
    def build(self):
        game = RocketGame()

        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game

if __name__ == '__main__':
    RocketApp().run()
