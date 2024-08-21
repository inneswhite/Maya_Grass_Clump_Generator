def tan_nrm_mat(name: str = "mat_tangent_nrm"):
    """Creates a material that renders the surface normals relative to the camera view

    Args:
        name (str): name of material

    Returns:
        list[material_node, shading_group_node]: an array containing both the generated material node and shading group node.
    """
    import pymel.core as pm

    # Check if normal material already exists
    if pm.PyNode(name):
        node = pm.PyNode(name)
        sg = node.shadingGroups()[0]
        return sg

    sampler_info = pm.shadingNode("samplerInfo", asUtility=True)

    nrm_mat = pm.shadingNode("aiFlat", asShader=True, name=name)
    nrm_sg = pm.sets(
        renderable=True, noSurfaceShader=True, empty=True, name=(name + "_SG")
    )

    sampler_info.normalCamera >> nrm_mat.color
    nrm_mat.outColor >> nrm_sg.surfaceShader
    return nrm_sg


def get_shading_group(obj):
    """Finds the first material applied to a given object,

    Args:
        obj: The Maya object to get a material from

    Raises:
        AttributeError: Material could not be found in shading group
        AttributeError: Shading group could not be found on object

    Returns:
        sg: the first shading group applied to the given object
    """
    import pymel.core as pm

    if hasattr(obj, "__len__"):
        raise Exception(
            f"Cannot get shading group on multiple objects.\n{obj} was given."
        )

    # get all shaders
    shading_engine = pm.ls(type="shadingEngine")

    # create a dictionary for shaders and meshes applied to them
    sg_mesh = {}
    for sg in shading_engine:
        sg_mesh[sg.name()] = sg.members(flatten=True)

    # cycle through dictionary, and look for a mesh match.
    for sg, meshes in sg_mesh.items():
        for mesh in meshes:
            # convert faces to meshes
            if isinstance(mesh, pm.MeshFace):
                mesh = mesh.node()

            # convert meshes to transforms
            if isinstance(mesh, pm.nt.Mesh):
                mesh = mesh.getTransform()

            if mesh == obj:
                return sg
    raise Exception(f"Could not find any materials applied to {obj}.")


def apply_shading_group(sg, obj):
    import pymel.core as pm

    if not pm.nodeType(sg) == "shadingEngine":
        raise Exception(f"{sg} is not of type 'shadingEngine' and cannot be applied.")
    pm.sets(sg, forceElement=obj)


def convert_to_unlit(material):
    import pymel.core as pm

    # create new material
    name = "tmp_unlit"
    unlit_mat = pm.shadingNode("aiFlat", asShader=True, name=name)
    unlit_sg = pm.sets(
        renderable=True, noSurfaceShader=True, empty=True, name=(name + "_SG")
    )

    albedo = pm.shadingNode()


def flat_albedo_mat(name):
    pass


if __name__ == "__main__":
    import pymel.core as pm

    get_shading_group(pm.selected()[0])
