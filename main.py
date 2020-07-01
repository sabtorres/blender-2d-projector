import bpy
import os

bl_info = {
    "name": "2D projector",
    "blender": (2, 82, 0),
    "category": "Object"
}

class RendererButton(bpy.types.Operator):
    bl_label = "Render"
    bl_idname = "wm.render_2d_animation"
    
    # class param defaults
    resolution_x = 1920
    resolution_y = 1080
    anti_aliasing = True
    transparency = True
    animation = False
    perspective = False
    output_path = os.getcwd() + "/output.png"
    
    def set_resolution(self, scene):
        scene.render.resolution_x = RendererButton.resolution_x
        scene.render.resolution_y = RendererButton.resolution_y
        scene.render.resolution_percentage = 100
    
    def set_anti_aliasing(self, scene):
        if RendererButton.anti_aliasing:
            scene.render.filter_size = 1.50
        else:
            scene.render.filter_size = 0
    
    def set_transparency(self, scene):
        scene.render.film_transparent = RendererButton.transparency
        
    def set_perspective(self):
        if RendererButton.perspective:
            bpy.data.cameras['Camera'].type = 'PERSP'
        else:
            bpy.data.cameras['Camera'].type = 'ORTHO'
    
    def set_output_path(self, scene):
        scene.render.filepath = RendererButton.output_path
    
    def execute(self, context):
        scene = context.scene
        scene.render.engine = 'BLENDER_EEVEE'
        
        self.set_resolution(scene)
        self.set_anti_aliasing(scene)
        self.set_transparency(scene)
        self.set_perspective()
        self.set_output_path(scene)
        
        bpy.ops.render.render(animation=RendererButton.animation, write_still=True)
        
        return { 'FINISHED' }   

class Animator(bpy.types.Menu):
    bl_description = "Blender 2D projector animator"
    bl_label = "2D Animator"
    bl_idname = "2D Animator"

    def draw(self, context):
        layout = self.layout
        #todo: sliders and checkboxes
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