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
    
    def set_resolution(self, scene):
        scene.render.resolution_x = scene.resolution_hor
        scene.render.resolution_y = scene.resolution_ver
        scene.render.resolution_percentage = 100
    
    def set_anti_aliasing(self, scene):
        if scene.anti_aliasing:
            scene.render.filter_size = 1.50
        else:
            scene.render.filter_size = 0
    
    def set_transparency(self, scene):
        scene.render.film_transparent = scene.transparency
        
    def set_perspective(self, scene):
        if scene.perspective:
            bpy.data.cameras['Camera'].type = 'PERSP'
        else:
            bpy.data.cameras['Camera'].type = 'ORTHO'
    
    def set_output_path(self, scene):
        scene.render.filepath = scene.output_path
    
    def execute(self, context):
        scene = context.scene
        scene.render.engine = 'BLENDER_EEVEE'

        self.set_resolution(scene)
        self.set_anti_aliasing(scene)
        self.set_transparency(scene)
        self.set_perspective(scene)
        self.set_output_path(scene)
        if not scene.animation:
            bpy.ops.render.render(write_still=True)
        else:
            object = context.object
            for action in bpy.data.actions:
                name = action.name
                object.animation_data.action = action
                for frame in range(scene.frame_start, scene.frame_end + 1):
                    scene.render.filepath = scene.output_path + name + '{:08d}.png'.format(frame)
                    scene.frame_set(frame)
                    bpy.ops.render.render(write_still=True)
        
        return { 'FINISHED' }   

class Animator(bpy.types.Panel):
    bl_description = "Blender 2D projector animator"
    bl_label = "2D Animator"
    bl_idname = "wm.2d_animator"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Tool"

    def draw(self, context):
        layout = self.layout
        
        scene = context.scene
        layout.prop(scene, "resolution_hor")
        layout.prop(scene, "resolution_ver")
        layout.prop(scene, "anti_aliasing")
        layout.prop(scene, "transparency")
        layout.prop(scene, "animation")
        layout.prop(scene, "perspective")
        layout.prop(scene, "output_path")
        
        layout.separator()
        layout.operator(RendererButton.bl_idname)

classes = [
    RendererButton,
    Animator
]

def register():
    bpy.types.Scene.resolution_hor = bpy.props.IntProperty(name="Resolution X", default=1920, soft_min=1, soft_max=1920)
    bpy.types.Scene.resolution_ver = bpy.props.IntProperty(name= "Resolution Y", default=1080, soft_min=1, soft_max=1080)
    bpy.types.Scene.anti_aliasing = bpy.props.BoolProperty(name="Anti Aliasing", default=True)
    bpy.types.Scene.transparency = bpy.props.BoolProperty(name="Transparency", default=True)
    bpy.types.Scene.animation = bpy.props.BoolProperty(name="Animation", default=False)
    bpy.types.Scene.perspective = bpy.props.BoolProperty(name="Perspective", default=False)
    bpy.types.Scene.output_path = bpy.props.StringProperty(name="Output Path", default="output.png")
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()