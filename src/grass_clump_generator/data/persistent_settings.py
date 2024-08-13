import configparser
import os
from grass_clump_generator.utils import strings

HEADER_UI_VALUES = "Generator UI Values"
HEADER_SOURCE_MESHES = "Source Meshes"


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


def read_value(section: str, key: str = "undefined"):
    config = configparser.ConfigParser()
    config.read(get_config_path())

    # return all values under section
    if key == "undefined":
        values = []
        keys = config.options(section)
        for _key in keys:
            values.append(config[section][_key])
        return values

    key = strings.space_to_underscore(key)
    if config.has_option(section, key):
        # check for bool values
        if config[section][key] == "True":
            return True
        if config[section][key] == "False":
            return False
        return config[section][key]
    else:
        print(f"Could not find '{key}' under the section, '{section}")
        return 0


def clear_section(section: str):
    config = configparser.ConfigParser()
    config.read(get_config_path())

    if config.has_section(section):
        for option in config.options(section):
            config.remove_option(section, option)
    else:
        print(
            f"Warning tried to access '{section}' section in grass_clump_generator_settings.ini that does not exist."
        )


def get_values_array(section: str):
    config = configparser.ConfigParser()
    config.read(get_config_path())

    values = []
    if config.has_section(section):
        for option in config.options(section):
            values.append(config[section][option])
    else:
        print(
            f"Warning tried to access '{section}' section in grass_clump_generator_settings.ini that does not exist."
        )
    return values
