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
    
    def render_frame(self, scene, frame):
        scene.render.filepath = scene.output_path + name + '{:08d}.png'.format(frame)
        scene.frame_set(frame)
        bpy.ops.render.render(write_still=True)
    
    def render_normals(self, scene, normal_material):
        # replace material data with normal maps
        original_materials = []
        for object in bpy.data.objects:
            if object.type == 'MESH':
                original_materials.append(object.active_material)
                object.data.materials.append(normal_material)
        
        # render
        scene.render.filepath = "normal_" + scene.render.filepath
        print("rendering...")
        bpy.ops.render.render(write_still=True)
        
        # todo: put the original materials back
        for object in bpy.data.objects:
            if object.type == 'MESH':
                object.data.materials.pop()
    
    def generate_normal_material(self):
        new_material = bpy.data.materials.new(name="Normal")
        new_material.use_nodes = True
        
        links = new_material.node_tree.links
        nodes = new_material.node_tree.nodes
        nodes.clear()
        
        geometry = nodes.new(type="ShaderNodeNewGeometry")
        
        vector_transform = nodes.new(type="ShaderNodeVectorTransform")
        vector_transform.convert_to = 'CAMERA'
        links.new(geometry.outputs[1], vector_transform.inputs[0])
        
        combine_xyz = nodes.new(type="ShaderNodeCombineXYZ")
        combine_xyz.inputs[0].default_value = 0.5
        combine_xyz.inputs[1].default_value = 0.5
        combine_xyz.inputs[2].default_value = -0.5
        
        multiply = nodes.new(type="ShaderNodeMixRGB")
        multiply.blend_type = "MULTIPLY"
        multiply.inputs[0].default_value = 1.0
        links.new(vector_transform.outputs[0], multiply.inputs[1])
        links.new(combine_xyz.outputs[0], multiply.inputs[2])
        
        add = nodes.new(type="ShaderNodeMixRGB")
        add.blend_type = 'ADD'
        add.inputs[0].default_value = 1.0
        links.new(multiply.outputs[0], add.inputs[1])
        add.inputs[2].default_value = (0.5, 0.5, 0.5, 1.0)
        
        rgb_curve = nodes.new(type="ShaderNodeRGBCurve")
        rgb_curve.mapping.curves[0].points[0].location = (0.0, 1.0)
        rgb_curve.mapping.curves[0].points[1].location = (1.0, 0.0)
        rgb_curve.inputs[0].default_value = 1.0
        links.new(add.outputs[0], rgb_curve.inputs[1])
        
        output = nodes.new(type="ShaderNodeOutputMaterial")
        links.new(rgb_curve.outputs[0], output.inputs[0])
        
        return new_material
    
    def execute(self, context):
        scene = context.scene
        scene.render.engine = 'BLENDER_EEVEE'
        
        material = self.generate_normal_material()

        self.set_resolution(scene)
        self.set_anti_aliasing(scene)
        self.set_transparency(scene)
        self.set_perspective(scene)
        self.set_output_path(scene)
        if not scene.animation:
            bpy.ops.render.render(write_still=True)
            if scene.normals:
                self.render_normals(scene, material)
        else:
            object = context.object
            for action in bpy.data.actions:
                name = action.name
                object.animation_data.action = action
                for frame in range(scene.frame_start, scene.frame_end + 1):
                    self.render_frame(scene, frame)
                    if scene.normals:
                        self.render_normals(scene, material)
        
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
        layout.prop(scene, "normals")
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
    bpy.types.Scene.normals = bpy.props.BoolProperty(name="Render Normals", default=False)
    bpy.types.Scene.output_path = bpy.props.StringProperty(name="Output Path", default="output.png")
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()