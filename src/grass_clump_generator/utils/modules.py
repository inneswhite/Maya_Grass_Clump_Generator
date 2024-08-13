import os
from importlib import reload, import_module
import sys
from grass_clump_generator.utils import paths, lists, strings
import grass_clump_generator.utils
import grass_clump_generator.utils.paths


def get_all_submodules(module) -> list[str]:
    """Returns a list of all sub modules under the given module using dot notation.

    Args:
        module (str or module): the name of the module to import submodules from

    Returns:
        list[str]: a list of all sub modules under the given module using dot notation
    """
    dir = os.path.abspath(paths.get_module_path(module))
    modules = []
    for root, directory, filename in os.walk(dir):
        for file in filename:
            if file.endswith(".py") and file != "__init__.py":
                file = file.replace(".py", "")
                rel_path = paths.diff_paths(dir, root)[0]
                modules.append(
                    str(module.__name__) + rel_path.replace("\\", ".") + "." + file
                )
    return modules


def reimport_modules(base_module):
    """Reimports all modules under a given directory

    Args:
        dir (str): Root directory from which to search for modules
    """
    print("\nReimporting all Python Modules... \n")

    # Iterate over all the files in the directory
    import_count = 0
    submodules = get_all_submodules(base_module)
    for module in submodules:
        # Import the module if it's not already imported
        if module in sys.modules:
            module = sys.modules[module]
        else:
            # Import the module (note: this assumes the module is in the directory or PYTHONPATH)
            module = import_module(module)
            import_count += import_count

        # Reload the module
        reload(module)
    print(
        f"Reloaded {str(len(submodules))} submodules.\nImported {import_count} new modules.\n"
    )


if __name__ == "__main__":
    import grass_clump_generator

    reload(grass_clump_generator.utils.paths)
    ##get_all_submodules(grass_clump_generator)
    print(
        paths.get_sub_dirs(
            r"C:\Users\Innes\Documents\GitRepos\Maya_Grass_Clump_Generator\src\grass_clump_generator"
        )
    )
