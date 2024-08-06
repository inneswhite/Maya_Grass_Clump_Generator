import configparser
import os
from grass_clump_generator.utils import strings

HEADER_UI_VALUES = "Generator UI Values"


def get_config_path():
    return os.path.join(os.path.dirname(__file__), "grass_clump_generator_settings.ini")


def write_value(header: str, key: str, value: str):
    config = configparser.ConfigParser()
    config.read(get_config_path())

    key = strings.space_to_underscore(key)

    if header in config:
        config[header][key] = value
    else:
        config[header] = {key: value}

    with open(get_config_path(), "w") as config_ini:
        config.write(config_ini)


def read_value(header: str, key: str):
    config = configparser.ConfigParser()
    config.read(get_config_path())

    key = strings.space_to_underscore(key)
    if config.has_option(header, key):
        return config[header][key]


def reset_preferences():
    pass
