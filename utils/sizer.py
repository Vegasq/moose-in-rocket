__author__ = 'vegasq'
from kivy.core.window import Window
import resources
from kivy.metrics import  dp, sp


class Sizer(object):
    def __init__(self):
        """
        rocket = Window.height / 6
        1 = rocket
        """
        point = Window.height / 8


    @staticmethod
    def _calc(part_from_screen, original_width, original_height,
              based_on_height=True):
        rocket_required_height = float(Window.height) / part_from_screen
        ratio = float(original_width) / original_height

        rocket_required_width = ratio * rocket_required_height
        return (rocket_required_width, rocket_required_height)

    @classmethod
    def get_rocket_size(cls):
        return resources.rocket['width'], resources.rocket['height']
        return cls._calc(
            10.0, resources.rocket['width'], resources.rocket['height'])

    @classmethod
    def get_asteroid_size(cls):
        return cls._calc(
            10.0, resources.asteroid['width'], resources.asteroid['height'])

    @classmethod
    def get_start_plate_size(cls):
        return cls._calc(
            10.0, resources.asteroid['width'], resources.asteroid['height'])

    @classmethod
    def get_screen_speed(cls):
        return int(Window.height / dp(150))

    @classmethod
    def get_rocket_speed(cls):
        return dp(5)
