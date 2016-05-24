bl_info = {
    "name": "My Pies",
    "author": "Stathis Sideris",
    "version": (1, 1, 0),
    "blender": (2, 72, 0),
    "description": "My Pie menus",
    "category": "Object" }

import bpy
from bpy.types import Menu, Operator

class VIEW3D_PIE_select_mode(Menu):
    bl_label  = "Select Mode"

    def draw(self, context):
        layout = self.layout

        pie = layout.menu_pie()
        # operator_enum will just spread all available options
        # for the type enum of the operator on the pie
        # pie.operator_enum("mesh.select_mode", "type")
        pie.operator("mesh.select_mode", text="Vertex", icon='VERTEXSEL').type = 'VERT'
        pie.operator("mesh.select_mode", text="Edge", icon='EDGESEL').type = 'EDGE'
        pie.operator("mesh.select_mode", text="Face", icon='FACESEL').type = 'FACE'

class ProportionalPoll(Operator):
    bl_idname = "pie.proportional"
    bl_label = "Proportional Poll"
    bl_options = {'INTERNAL'}
    mode = bpy.props.StringProperty()

    @classmethod
    def poll (cls, context):
        return True

    def execute(self, context):
        bpy.context.scene.tool_settings.proportional_edit = self.mode
        return {'FINISHED'}

class VIEW3D_PIE_proportional_editing(Menu):
    bl_label = "Proportional editing"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        pie.operator("pie.proportional", text="Enabled", icon='PROP_ON').mode = 'ENABLED'
        pie.operator("pie.proportional", text="Disabled", icon='PROP_OFF').mode = 'DISABLED'
        pie.operator("pie.proportional", text="Projected (2D)", icon='PROP_ON').mode = 'PROJECTED'
        pie.operator("pie.proportional", text="Connected", icon='PROP_CON').mode = 'CONNECTED'

class FalloffPoll(Operator):
    bl_idname = "pie.falloff"
    bl_label = "Falloff Poll"
    bl_options = {'INTERNAL'}
    falloff = bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        if bpy.context.scene.tool_settings.proportional_edit == 'DISABLED':
            bpy.context.scene.tool_settings.proportional_edit = 'ENABLED'
        bpy.context.scene.tool_settings.proportional_edit_falloff = self.falloff
        return {'FINISHED'}

class FalloffPie(Menu):
    bl_label = "Proportional falloff"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        pie.operator("pie.falloff", text="Sphere", icon="SPHERECURVE").falloff = 'SPHERE'
        pie.operator("pie.falloff", text="Root", icon="ROOTCURVE").falloff = 'ROOT'
        pie.operator("pie.falloff", text="Smooth", icon="SMOOTHCURVE").falloff = 'SMOOTH'
        pie.operator("pie.falloff", text="Linear", icon="LINCURVE").falloff = 'LINEAR'
        pie.operator("pie.falloff", text="Constant", icon="NOCURVE").falloff = 'CONSTANT'
        pie.operator("pie.falloff", text="Inverse Square", icon="ROOTCURVE").falloff = 'INVERSE_SQUARE'
        pie.operator("pie.falloff", text="Sharp", icon="SHARPCURVE").falloff = 'SHARP'
        pie.operator("pie.falloff", text="Random", icon="RNDCURVE").falloff = 'RANDOM'
        pie.operator("pie.proportional", text="Disable", icon="PROP_OFF").mode = 'DISABLED'

addon_keymaps = [] # Store keymaps to use in unregister()

classes = (
    VIEW3D_PIE_select_mode,
    ProportionalPoll,
    FalloffPoll,
    FalloffPie,
    VIEW3D_PIE_proportional_editing
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    # Define a keyboard shortcut (for Mesh Edit mode)
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name="Mesh")
    kmi = km.keymap_items.new("wm.call_menu_pie", 'TAB', 'PRESS', shift=False, ctrl=True)
    kmi.properties.name="VIEW3D_PIE_select_mode"
    kmi = km.keymap_items.new("wm.call_menu_pie", 'O', 'PRESS', shift=False, ctrl=False)
    kmi.properties.name="VIEW3D_PIE_proportional_editing"
    kmi = km.keymap_items.new('wm.call_menu_pie', 'O', 'PRESS', shift=True)
    kmi.properties.name = "FalloffPie"
    addon_keymaps.append(km)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    wm = bpy.context.window_manager

    #use stored keymaps to unregister
    for km in addon_keymaps:
        for kmi in km.keymap_items:
            km.keymap_items.remove(kmi)
        wm.keyconfigs.addon.keymaps.remove(km)

if __name__ == "__main__":
    register()
