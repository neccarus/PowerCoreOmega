from guipyg.utils.utils import Instance
from src.controls import Controls
import json
import pygame


class Settings(Instance):

    def __init__(self, controls=None, screensize=(1600, 900), fullscreen=False):
        self.controls = controls
        self.screensize = screensize
        self.fullscreen = fullscreen

    @classmethod
    def load_settings(cls, file_name):
        with open(file_name, 'r') as read_file:
            settings_json = json.load(read_file)

        # print(settings_json)
        # if hasattr(settings_json, 'controls'):
        for obj in settings_json['controls']:
            settings_json['controls'][obj] = Controls.Signal(settings_json['controls'][obj].values())
        settings_json['controls'] = Controls(settings_json['controls'].values())
        # TODO: FIX THIS BUG!!!
        print(settings_json['controls'].signals['forward'].__dict__)

        return cls._decode_settings(settings_json)

    @classmethod
    def _decode_settings(cls, settings_json):
        setting_obj = Settings(**settings_json)
        return setting_obj

    @classmethod
    def save_new_settings(cls, file_name, settings):
        with open(file_name, 'w') as write_file:
            json.dump(settings, write_file, cls=cls.SettingsEncoder)

    @classmethod
    def save_over_settings(cls, file_name, settings):
        old_settings = cls.load_settings(file_name).__dict__
        merged_settings = {**old_settings, **settings}
        with open(file_name, 'w') as write_file:
            json.dump(merged_settings, write_file, cls=cls.SettingsEncoder)

    class SettingsEncoder(json.JSONEncoder):

        def default(self, o):
            # if hasattr(o, 'controls'):
            #     o.function = self._encode_controls(o.function)
            if hasattr(o, 'controls'):
                del o.controls.signals
            return o.__dict__

        @staticmethod
        def _encode_controls(function):
            encoded_controls = {
                'forward': function.signals['forward'],
                'backward': function.signals['backward'],
                'left': function.signals['left'],
                'right': function.signals['right'],
                'fire_weapon': function.signals['fire_weapon'],
                'eject_heat_sink': function.signals['eject_heat_sink'],
                'boost_shields': function.signals['boost_shields'],
            }
            return encoded_controls


def clamp(num, smallest, largest):
    return max(smallest, min(num, largest))


setting_defaults = {
    'controls': Controls(),
    'screensize': (1600, 900),
    'fullscreen': False,
}
