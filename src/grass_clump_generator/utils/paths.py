import pymel.core as pm
import os
import sys
import glob


def get_module_path(module) -> str:
    return os.path.dirname(module.__file__)


def get_maya_project_dir():
    return pm.workspace.getPath()


def get_maya_scripts_dir():
    return os.path.join(get_maya_project_dir(), "scripts")


def get_maya_images_dir() -> str:
    """Returns the Project Images directory path

    Returns:
        str: Maya Project Images directory path
    """
    return os.path.join(get_maya_project_dir(), "images")


def get_maya_temp_images_dir() -> str:
    dir = os.path.join(get_maya_images_dir(), "temp")
    if not os.path.exists(dir):
        os.makedirs(dir)
    return dir


def find_matching_files(dir, pattern):
    search_pattern = os.path.join(dir, pattern)
    return glob.glob(search_pattern)


def get_sub_dirs(dir):
    sub_dirs = []
    for child in os.listdir(dir):
        if not "." in child and not "__pycache__" in child:
            sub_dirs.append(child)
    return sub_dirs


def diff_paths(path1: str, path2: str) -> list[str]:
    """Compares two paths and returns a list of the strings that are unique to the given path

    Args:
        path1 (str): The first path to compare for diff
        path2 (str): the second path to compare for diff

    Returns:
        list[str]: [path1 - path2, path2 - ath1]
    """

    return [path2.replace(path1, ""), path2.replace(path1, "")]


def open_path(path: str):
    """Files will be run, directories will be opened in explorer

    Args:
        file (str): path to file or directory
    """
    os.startfile(path)


def clear_directory(path: str):
    """_summary_

    Args:
        path (str): _description_
    """
    if os.path.exists(path) and os.path.isdir(path):
        for file in os.listdir(path):
            file_path = os.path.join(path, file)
            os.unlink(file_path)
    else:
        raise Exception(f"{path} does not exist, or is not a directory.")
