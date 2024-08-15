# import pymel.core as pm
import random
import math
from grass_clump_generator.rendering.camera import BillboardCameras
import grass_clump_generator.rendering.render as renderer
import grass_clump_generator.data.persistent_settings as ps
from .utils import paths


def lerp(min, max, blend):
    return min + (min - max) * blend


class GrassClumpGenerator:
    def __init__(
        self,
        foliage_arr=["undefined"],
        total_foliage_count: int = 100,
        distribution_radius: float = 5,
        rotation_variation: float = 360,
        scale_variation: float = 20,
        scale_distance: float = 20,
    ):
        import pymel.core as pm

        foliage_names = ps.read_value(ps.HEADER_SOURCE_MESHES)
        self.foliage_values = []
        self.foliage_objs = []
        if foliage_arr == ["undefined"]:
            for name in foliage_names:
                self.foliage_objs.append(pm.PyNode(name))
                self.foliage_values.append(
                    int(ps.read_value(ps.HEADER_UI_VALUES, name))
                )
        self.total_foliage_count = total_foliage_count
        self.distribution_radius = distribution_radius
        self.rotation_variation = rotation_variation
        self.scale_variation = scale_variation
        self.scale_distance = scale_distance

    def convert_ratio_decimal(self, ratios: list[int]) -> list[float]:
        ratio_total = sum(ratios)
        decimals = []
        for i in ratios:
            decimals.append(i / ratio_total)

        return decimals

    def calculate_number_of_foliage(
        self, foliage_ratios: list[int], total_count: int
    ) -> list[int]:
        """Returns a list containing how many instances each piece of foliage should be created from a given list of foliage.

        Args:
            foliage_ratios (list[int]): A list of probabilities ranging from 0-100 for likely a piece of foliage should spawn.
            total_count (int): The total number of foliage pieces to be generated

        Returns:
            list[int]: A list of the same length as the input ratios list, but with the number of each foliage that should be created.
        """
        foliage_decimals = self.convert_ratio_decimal(foliage_ratios)
        print(f"\nFoliage Decimals = {foliage_decimals}\nTotal Count = {total_count}")
        foliage_count = []
        for decimal in foliage_decimals:
            foliage_count.append(round(float(decimal) * float(total_count)))
        return foliage_count

    def create_instances(self, target_foliage_numbers: list) -> list:
        """Creates instances from a list containing how many of each foliage should be generated

        Args:
            target_foliage_numbers (list): Target number of foliage to be generated for each foliage type

        Returns:
            list: an array containing a cell for each foliage type, with a sub-array containing all generated instances
        """
        import pymel.core as pm

        # create empty array with a length of the number of foliage types
        foliage_instances = [[] for i in range(len(target_foliage_numbers))]
        # for each foliage type create an empty sub array
        for foliage_type_i in range(len(foliage_instances)):
            # for each type, create the same number of instances
            foliage_type_obj = self.foliage_objs[foliage_type_i]
            for instance_index in range(target_foliage_numbers[foliage_type_i]):
                _instance = pm.duplicate(foliage_type_obj)
                pm.parent(_instance, world=True)
                foliage_instances[foliage_type_i].append(_instance[0])
        print(f"foliage instances {foliage_instances}")
        return foliage_instances

    def position_instance(self, foliage_instance, radius: float):
        """Give a given instance a random position within a radius

        Args:
            foliage_instance (foliage_obj): A single foliage instance
            radius (float): The maximum distance from origin a foliage instance can be
        """
        random_radius = random.uniform(0, radius)
        random_radian = random.uniform(0, 2 * math.pi)
        x_pos = random_radius * math.cos(random_radian)
        z_pos = random_radius * math.sin(random_radian)
        foliage_instance.translate.set(x_pos, 0, z_pos)

    def rotate_instance(self, foliage_instance, rotation_variation):
        import pymel.core as pm

        random_rotation = random.uniform(
            -1 * (rotation_variation * 0.5), rotation_variation * 0.5
        )
        pm.rotate(foliage_instance, (0, random_rotation, 0))

    def scale_instance(self, foliage_instance, scale_variation, scale_distance):
        # randomise scaling uniformly
        import pymel.core as pm

        nrml_scale = scale_variation * 0.01
        random_scale = random.uniform(1 - (nrml_scale), 1)

        # scale by distance to center of clump
        instance_pos = pm.xform(
            foliage_instance, query=True, translation=True, worldSpace=True
        )
        vec_pos = pm.dt.Vector(instance_pos)
        distance_scale = lerp(
            (1 - (vec_pos.length() / self.distribution_radius)),
            1,
            (scale_distance * 0.01),
        )

        combined_scale = (random_scale + distance_scale) * 0.5

        pm.scale(foliage_instance, (1, combined_scale, 1))

    def transform_instances(self, foliage_instances):
        for foliage_index in range(len(foliage_instances)):
            for _instance in foliage_instances[foliage_index]:
                self.position_instance(_instance, self.distribution_radius)
                self.rotate_instance(_instance, self.rotation_variation)
                self.scale_instance(
                    _instance, self.scale_variation, self.scale_distance
                )

    def merge_instances(self, foliage_instances):
        """Merges all the individual foliage pieces into one clump.

        Args:
            foliage_instances (list): list of all foliage pieces to be merged

        Returns:
            pm.transform: Merged grass clump
        """
        import pymel.core as pm

        name = "Generated_Veg_Clump"
        pm.select(deselect=True)
        pm.select(foliage_instances)
        print(f"Instances for combine are {foliage_instances} \n")
        return pm.polyUnite(constructionHistory=False, name=name)

    def generate(self):
        """Begin Grass Clump Generation

        Returns:
            pm.transform: Grass Clump
        """

        print(f"Generating foliage from {self.foliage_objs}")
        # Calculate foliage ratios from UI values
        target_foliage_ratios = self.calculate_number_of_foliage(
            self.foliage_values, self.total_foliage_count
        )

        # Grass Clump mesh
        self.foliage_instances = self.create_instances(target_foliage_ratios)

        self.transform_instances(self.foliage_instances)
        return self.merge_instances(self.foliage_instances)
