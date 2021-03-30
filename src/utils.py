from guipyg.utils.utils import Instance
from src.controls import Controls
import json


class Settings(Instance):

    def __init__(self, controls=None, screensize=(1600, 900), fullscreen=False):
        self.controls = controls
        self.screensize = screensize
        self.fullscreen = fullscreen

    @classmethod
    def load_settings(cls, file_name):
        with open(file_name, 'r') as read_file:
            settings_json = json.load(read_file)

        for signal in settings_json['controls'].keys():
            if 'inputs' in settings_json['controls'][signal].keys():
                settings_json['controls'][signal] = settings_json['controls'][signal]['inputs']
        settings_json['controls'] = Controls(**settings_json['controls'])

        return cls._decode_settings(settings_json)

    @classmethod
    def _decode_settings(cls, settings_json):
        setting_obj = Settings(**settings_json)
        print(setting_obj.controls)
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
            return o.__dict__

        @staticmethod
        def _encode_controls(control):
            encoded_controls = {
                'forward': control.forward,
                'backward': control.backward,
                'left': control.left,
                'right': control.right,
                'fire_weapon': control.fire_weapon,
                'eject_heat_sink': control.eject_heat_sink,
                'boost_shields': control.boost_shields,
            }
            return encoded_controls


def clamp(num, smallest, largest):
    return max(smallest, min(num, largest))


setting_defaults = {
    'controls': Controls(),
    'screensize': (1600, 900),
    'fullscreen': False,
}
