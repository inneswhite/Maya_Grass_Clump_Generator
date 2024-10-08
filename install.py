import os
import sys
import maya


def onMayaDroppedPythonFile(arg):
    srcDir = os.path.join(os.path.dirname(__file__), "src")
    iconDir = os.path.join(
        os.path.dirname(__file__), "resources", "icons", "button_icon.png"
    )

    srcDir = os.path.normpath(srcDir)
    iconDir = os.path.normpath(iconDir)

    # Check if tool is installed
    if srcDir not in sys.path:
        sys.path.insert(0, srcDir)

    button_command = """
from importlib import reload
import sys

if r'{dir}' not in sys.path:
    sys.path.insert(0, r'{dir}')

import grass_clump_generator
reload(grass_clump_generator)
grass_clump_generator.start()
    """.format(
        dir=srcDir
    )
    shelf = maya.mel.eval("$gShelfTopLevel=$gShelfTopLevel")
    parent = maya.cmds.tabLayout(shelf, query=True, selectTab=True)
    maya.cmds.shelfButton(
        command=button_command,
        annotation="Grass Clump",
        sourceType="Python",
        image=iconDir,
        image1=iconDir,
        parent=parent,
    )
