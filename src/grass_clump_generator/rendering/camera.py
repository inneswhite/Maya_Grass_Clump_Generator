import math


class BillboardCameras:
    def __init__(self, orthographicWidth: float = 50) -> None:
        self.orthographicWidth = orthographicWidth

        self.front_camera = None
        self.right_camera = None

    def set_orthographic_size(self, scale: float = 50):
        import pymel.core as pm

        pm.setAttr(self.front_camera[1] + ".orthographicWidth", scale)
        pm.setAttr(self.right_camera[1] + ".orthographicWidth", scale)

    def transform_cameras(
        self,
        front_camera_pos: list = [0, 0, 1000],
        right_camera_pos: list = [1000, 0, 0],
        front_camera_rot: list = [0, 0, 0],
        right_camera_rot: list = [0, 90, 0],
    ):
        import pymel.core as pm

        print(f"Moving {self.front_camera[0]} to {front_camera_pos}")
        pm.move(self.front_camera[0], front_camera_pos)
        pm.move(self.right_camera[0], right_camera_pos)

        pm.rotate(self.front_camera[0], front_camera_rot)
        pm.rotate(self.right_camera[0], right_camera_rot)

    def create_cameras(self):
        import pymel.core as pm

        self.front_camera = pm.camera(
            name="Camera_Front_Foliage",
            aspectRatio=1,
            displayResolution=True,
            orthographic=True,
        )
        self.right_camera = pm.camera(
            name="Camera_Right_Foliage",
            aspectRatio=1,
            displayResolution=True,
            orthographic=True,
        )

        return [self.front_camera, self.right_camera]

    def fit_to_target(self, target, res_width, res_height):
        import pymel.core as pm

        print(f"Fitting {self.front_camera}'s view to {target}")

        # adjust orthographic width
        bounding_min = pm.getAttr(target[0] + ".boundingBoxMin")
        bounding_max = pm.getAttr(target[0] + ".boundingBoxMax")
        print(f"bounding min = {bounding_min}, bounding max = {bounding_max}")

        height = abs(bounding_min[1] - bounding_max[1])
        width = abs(bounding_min[0] - bounding_max[0])
        depth = abs(bounding_min[2] - bounding_max[2])

        max_width = max(width, depth)

        aspect_ratio = res_width / res_height

        ortho_width = 2  # padding
        if res_width > res_height:
            if height > max_width:
                ortho_width = ortho_width + height * aspect_ratio
            elif max_width > height:
                ortho_width = ortho_width + height * aspect_ratio
        elif res_height > res_width:
            if max_width > height:
                ortho_width = ortho_width + height / aspect_ratio
            elif height > max_width:
                ortho_width = ortho_width + max_width

        pm.setAttr(self.front_camera[1] + ".orthographicWidth", ortho_width)
        pm.setAttr(self.right_camera[1] + ".orthographicWidth", ortho_width)

        # align camera position
        pm.select(target)

        pm.move(self.front_camera[0], 0.5 * height, moveY=True, relative=True)
        pm.move(self.right_camera[0], 0.5 * height, moveY=True, relative=True)

        # pm.viewFit(self.front_camera, all=False)
        # pm.viewFit(self.front_camera, all=False)

    def generate(self):
        self.create_cameras()
        self.transform_cameras()
        self.set_orthographic_size(self.orthographicWidth)

    def get_cameras(self) -> list:
        return [self.front_camera, self.right_camera]


if __name__ == "__main__":
    billboardCameras = BillboardCameras(orthographicWidth=50)
    billboardCameras.generate()
