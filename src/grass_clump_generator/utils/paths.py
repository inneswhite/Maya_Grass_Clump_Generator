import pymel.core as pm
import os
import sys


def get_project_dir():
    return pm.workspace.getPath()


def get_scripts_dir():
    return os.path.join(get_project_dir(), "scripts")


def get_images_dir():
    return os.path.join(get_project_dir(), "images")


print(get_scripts_dir())
for subdir, dirs, files in os.walk(get_scripts_dir()):
    print(subdir)
    sys.path.append(subdir)
