import grass_clump_generator.rendering.camera
from grass_clump_generator.rendering.camera import BillboardCameras
import maya.cmds as cmds
from grass_clump_generator.utils import paths
import os


def load_and_configure_arnold_render():
    """Credit to VVVSLAVA on Tech-artist.org
    #https://discourse.techart.online/t/render-a-single-frame-in-maya-with-arnold-not-working/16490/2

    Ensures Arnold is installed and appropriate nodes are present in Maya scene

    Returns:
        int: exit code - 0-success, 1-failed
    """
    import pymel.core as pm

    # Check that IPR and Batch is not running. Otherwise - cancel:
    try:
        pm.arnoldRenderView(opt=("Run IPR", "False"))
    except:
        pass
    try:
        pm.batchRender()
    except:
        pass
    if "mtoa" in pm.moduleInfo(listModules=True):
        # load mtoa if not already loaded
        if not pm.pluginInfo("mtoa", query=True, loaded=True):
            try:
                pm.loadPlugin("mtoa", quiet=True)

                from mtoa.core import createOptions

                if not pm.objExists("defaultArnoldRenderOptions"):
                    createOptions()

                pm.setAttr("defaultArnoldRenderOptions.render_device_fallback", 1)
                pm.setAttr("defaultArnoldRenderOptions.renderDevice", 0)
                pm.setAttr("defaultArnoldRenderOptions.abortOnError", 0)
            except Exception:
                print(f"\n{pm.stackTrace()}")
                print("\nError loading Arnold MtoA Plugin !!!")
                return 1
            else:
                return 0
        else:
            try:
                from mtoa.core import createOptions

                createOptions()
                pm.setAttr("defaultArnoldRenderOptions.render_device_fallback", 1)
                pm.setAttr("defaultArnoldRenderOptions.renderDevice", 0)
                pm.setAttr("defaultArnoldRenderOptions.abortOnError", 0)
                pm.arnoldFlushCache(flushall=True)
            except Exception:
                print(f"\n{pm.stackTrace()}")
                print("\nError while configuring Arnold")
                return 1
            else:
                return 0
    else:
        print("Could not find MtoA plugin.")
        return 1


def prerender_settings(
    camera_name: str,
    output_dir: str,
    image_base_name: str = "clump_render",
    image_format: str = "exr",
    width: int = 512,
    height: int = 512,
):
    """Credit to VVVSLAVA on Tech-artist.org
    #https://discourse.techart.online/t/render-a-single-frame-in-maya-with-arnold-not-working/16490/2

    Args:
        output_dir (str): Path to where renders should be exported to
        image_base_name (str): Base name for render export
        camera_name (str): Name of camera to render from
        image_format (str, optional): Image formate for render export. Defaults to "exr".
        width (int, optional): Render width in pixels. Defaults to 512.
        height (int, optional): Render height in pixels. Defaults to 512.

    Returns:
        bool: True if pre render settings configured successfully
    """

    import pymel.core as pm

    # Create output dir if not exists.
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    # Create output file name with camera name and resolution parametrs.
    output_file_base_name = ("{}__cam_{}_{}x{}_frame").format(
        image_base_name, camera_name, str(width), str(height)
    )

    if load_and_configure_arnold_render() == 0:
        # Set "defaultArnoldRenderOptions" "renderGlobals" attribute from "defaultRenderGlobals" node attributes.
        pm.setAttr(
            "defaultArnoldRenderOptions.renderGlobals",
            "defaultRenderGlobals",
            type="string",
        )

        # Set "defaultArnoldDriver" attribut for output render file format ("exr").
        pm.setAttr("defaultArnoldDriver.aiTranslator", image_format, type="string")
        pm.setAttr("defaultArnoldDriver.outputMode", 2)
        pm.setAttr("defaultArnoldDriver.exrCompression", 0)
        pm.setAttr("defaultArnoldDriver.colorManagement", 2)

        # resolution
        pix_aspect = width / height
        pix_device_aspect = pm.getAttr("defaultResolution.deviceAspectRatio")

        pm.setAttr("defaultResolution.width", width)
        pm.setAttr("defaultResolution.height", height)
        pm.setAttr("defaultResolution.pixelAspect", pix_aspect)
        pm.setAttr("defaultResolution.deviceAspectRatio", pix_aspect)

        # Set defaultRenderGlobals attributes for prefix (replace default render path)
        pm.setAttr(
            "defaultRenderGlobals.imageFilePrefix", output_file_base_name, type="string"
        )
        pm.setAttr("defaultRenderGlobals.useFrameExt", 1)
        pm.setAttr("defaultRenderGlobals.useMayaFileName", 1)

        # Set defaultRenderGlobals attributes for naming with frame ext.
        pm.setAttr("defaultRenderGlobals.animation", 1)
        pm.setAttr("defaultRenderGlobals.outFormatControl", 0)
        pm.setAttr("defaultRenderGlobals.putFrameBeforeExt", 1)
        pm.setAttr("defaultRenderGlobals.periodInExt", 2)
        pm.setAttr("defaultRenderGlobals.extensionPadding", 4)

        # Set defaultRenderGlobals attributes for animation range
        pm.setAttr("defaultRenderGlobals.animationRange", 0)
        return True
    else:
        print(f"\n{pm.stackTrace()}")
        pm.error("\nError loading Arnold")
        raise Exception("\nError loading Arnold")


if __name__ == "__main__":
    from importlib import reload
    import pymel.core as pm

    reload(grass_clump_generator.rendering.camera)
