class BillboardCameras():
    def __init__(self, orthographicWidth:float=50) -> None:
        self.orthographicWidth = orthographicWidth

        self.front_camera = None
        self.right_camera = None

    def set_orthographic_size(self, scale:float=50):
        import pymel.core as pm

        pm.setAttr(self.front_camera[1] + ".orthographicWidth", scale)
        pm.setAttr(self.right_camera[1] + ".orthographicWidth", scale)
        
    def transform_cameras(self, front_camera_pos:list=[0,0,100], right_camera_pos:list=[100,0,0], front_camera_rot:list=[0,0,0], right_camera_rot:list=[0,90,0]):
        import pymel.core as pm

        pm.move(self.front_camera[0], front_camera_pos)
        pm.move(self.right_camera[0], right_camera_pos)

        pm.rotate(self.front_camera[0], front_camera_rot)
        pm.rotate(self.right_camera[0], right_camera_rot)

    def create_cameras(self):
        import pymel.core as pm

        self.front_camera = pm.camera(name="Camera_Front_Foliage")
        self.right_camera = pm.camera(name="Camera_Right_Foliage")

        pm.setAttr(self.front_camera[1] + ".orthographic", True)
        pm.setAttr(self.right_camera[1] + ".orthographic", True)

    def generate(self):
        self.create_cameras()
        self.transform_cameras()
        self.set_orthographic_size(self.orthographicWidth)

    def get_cameras(self)-> list:
        return [self.front_camera, self.right_camera]


        

if __name__ == "__main__":
    billboardCameras = BillboardCameras(orthographicWidth=50)
    billboardCameras.generate()