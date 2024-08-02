import grass_clump_generator.rendering.camera
from grass_clump_generator.rendering.camera import BillboardCameras
import mtoa.cmds as mtoa

class BillboardRender():
    def __init__(self, cameras:list):
        self.front_camera = cameras[0]
        self.right_camera = cameras[1]
    
    def render(self, resolution:list=[512,512]):
        import pymel.core as pm
        pm.lookThru(self.front_camera[1])
        pm.render(self.front_camera[1], x=resolution[0], y=resolution[1])
    

if __name__ == "__main__":
    from importlib import reload
    reload(grass_clump_generator.rendering.camera)

    camera_render = BillboardCameras()
    camera_render.create_cameras()
    print(camera_render.get_cameras())
    billboard_render = BillboardRender(camera_render.get_cameras())
    billboard_render.render([512, 512])