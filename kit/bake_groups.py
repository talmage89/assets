"""Optional projection isolation, preserving object-space procedural coordinates."""
from mathutils import Vector


def owner(ob,roots):
    while ob:
        if ob.name in roots:return ob.name
        ob=ob.parent
    return 'stationary'


def offsets(objects,roots,padding=.1):
    points=[ob.matrix_world@Vector(c) for ob in objects for c in ob.bound_box]
    span=max(p.x for p in points)-min(p.x for p in points)+padding
    return {'stationary':Vector((0,0,0)),**{name:Vector((span*(i+1),0,0)) for i,name in enumerate(roots)}}


def referenced_frames(objects,roots):
    """Snapshot explicit shader coordinate frames before isolation detaches meshes.

    Default Object coordinates follow the mesh automatically. Explicit Object
    references need the owning module's translation too. Snapshot every frame
    before changing any parent, including nested node groups and helper frames.
    """
    found=set();visited=set()
    def visit(tree):
        if tree in visited:return
        visited.add(tree)
        for node in tree.nodes:
            if node.type=='TEX_COORD' and node.object:found.add(node.object)
            if node.type=='GROUP' and node.node_tree:visit(node.node_tree)
    for ob in objects:
        for material in ob.data.materials:
            if material and material.use_nodes:visit(material.node_tree)
    return [(ob,ob.matrix_world.copy(),owner(ob,roots)) for ob in found]


def translate_frames(frames,spacing):
    for ob,world,group in frames:
        if group=='stationary':continue
        ob.parent=None;ob.matrix_world=world
        ob.matrix_world.translation+=spacing[group]
