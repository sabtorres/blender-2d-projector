import bpy

bl_info = {
    "name": "2D projector",
    "blender": (2, 82, 0),
    "category": "Object"
}

class RendererButton(bpy.types.Operator):
    bl_label = "Renderer Button"
    bl_idname = "wm.render_2d_animation"
    
    # class param defaults
    resolution_x = 1920
    resolution_y = 1080
    anti_aliasing = True
    filtering = True
    transparency = True
    animation = False
    output_path = "output.png"
    
    def execute(self, context):
        #todo: setup
        bpy.ops.render.render()
        
        return { 'FINISHED' }   

class Animator(bpy.types.Menu):
    bl_description = "Blender 2D projector animator"
    bl_label = "2D Animator"
    bl_idname = "2D Animator"

    def draw(self, context):
        layout = self.layout
        layout.separator()
        layout.operator(RendererButton.bl_idname)

classes = [
    RendererButton,
    Animator
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()