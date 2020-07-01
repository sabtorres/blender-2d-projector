import bpy

bl_info = {
    "name": "2D projector",
    "blender": (2, 82, 0),
    "category": "Object"
}

class Animator(bpy.types.Menu):
    bl_description = "Blender 2D projector animator"
    bl_label = "2D animator"

def register():
    bpy.utils.register_class(Animator)


def unregister():
    bpy.utils.unregister_class(Animator)


if __name__ == "__main__":
    register()