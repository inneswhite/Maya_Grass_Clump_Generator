import configparser
import os


def get_config_path():
    return os.path.join(os.path.dirname(__file__), "grass_clump_generator_settings.ini")


def write_value(header: str, key: str, value: str):
    config = configparser.ConfigParser()
    config.read(get_config_path())

    if header in config:
        config[header][key] = value
    else:
        config[header] = {key: value}

    with open(get_config_path(), "w") as config_ini:
        config.write(config_ini)
