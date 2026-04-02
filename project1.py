import maya.cmds as cmds
from PySide6 import QtWidgets, QtCore
import maya.OpenMayaUI as omui
from shiboken6 import wrapInstance
# cake generator!
# parameters: cake levels (integer), cake height (float), cake width (float),
# cake color (???), icing (boolean), cake level proportion (float)
# first I need to get Maya to generate a cylinder.
# We'll call this function generate_level


def get_maya_main_win():
    """Return the Maya main window widget"""
    main_window = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window), QtWidgets.QWidget)


class Cake():

    levels = 5
    cake_height = 3.0
    cake_width = 1.0
    level_proportion = 0.75
    cake_color = "red"
    icing = True
    
    def generate_level(self, level, level_width, level_height):
        level_lift = level*level_height
        lvl_name = cmds.polyCylinder(height=level_height,
                                     radius=level_width)[0]
        cmds.xform(lvl_name, pivots=[0, -level_height/2, 0])
        cmds.xform(lvl_name, translation=[0, level_height, 0])
        cmds.xform(lvl_name, translation=[0, level_lift+(0.5*level_height), 0])
        Cake._freeze_transforms(self, lvl_name)
        return lvl_name

    def generate_icing(self, level_width, level_height, level):
        level_lift = level*level_height
        icing_name = cmds.polyTorus(radius=level_width, sectionRadius=0.1*(self.level_proportion**level))[0]
        cmds.xform(icing_name, translation=[0,
                   level_lift+level_height, 0])
        return icing_name

    def calculate_width(self, level):
        # this is where we apply the level_proportion to the cake level.
        # we want the levels to get progressively smaller as they increase.
        # on level 0, we want the width to be unchanged.
        # level_width = cake_width
        level_width = (self.level_proportion**level)*self.cake_width
        return level_width
    
    def color_cake(self, grp_name):
        cmds.select(grp_name, replace=True)
        shader_name = cmds.shadingNode("standardsurface",
                                       asShader=True, name="cakeShader",)[0]
        sg_name = f"{shader_name}SG"
        cmds.sets(renderable=True, noSurfaceShader=True,
                  empty=True, name=sg_name)
        cmds.connectAttr(shader_name.outColor,
                         sg_name.surfaceShader, force=True)
        cmds.hyperShade(assign=shader_name)

# testing this in maya (reminder for later in case we lose SE again:)
#         import maya.cmds as cmds
# cmds.select("cake_GRP", replace=True)
# shader_name = cmds.shadingNode("standardsurface", asShader=True, name="cakeShader")
# sg_name = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name="cakeShaderSG")[0]
# cmds.connectAttr("%s.outColor" % shader_name, "%s.surfaceShader" % sg_name, force=True)
# cmds.hyperShade(assign=shader_name)

# I'll need to call generate_level multiple times.
# I can call this in another function, generate_cake.
    def generate_cake(self):
        cake_list = []
        level_height = self.cake_height/float(self.levels)
        for level in range(0, self.levels):
            level_width = Cake.calculate_width(self, level)
            lvl_name = Cake.generate_level(self, level,
                                           level_width, level_height)
            cake_list.append(lvl_name)
            if self.icing is True:
                icing_name = Cake.generate_icing(self, level_width,
                                                 level_height, level)
                cake_list.append(icing_name)
        grp_name = cmds.group(cake_list, name='cake_GRP')
        cmds.xform(grp_name, pivots=[0, 0, 0])
        if self.cake_color != "white":
            Cake.color_cake(self, grp_name)

    def _freeze_transforms(self, obj_name):
        cmds.makeIdentity(obj_name, apply=True, translate=True,
                          rotate=True, scale=True, normal=False,
                          preserveNormals=True)
        

class CakeWin(QtWidgets.QDialog):
    def __init__(self):
        super(CakeWin, self).__init__(parent=get_maya_main_win())
        self.setWindowTitle("Cake Generator")
        self.resize(500, 200)


### notes from class 3/30/26:
# from PySide6 import QtWidgets, QtCore
# class CakeWin(QtWidgets.QDialog):
#     def __init__(self):
#          super().__init__()
#          self.setWindowTitle("Cake Generator")
#          self.resize(500,200)
#
#
# in maya: create CakeWin object
# win = project1.CakeWin()
# win.show###

# in maya script editor:
# import project1
# import importlib
# importlib.reload(project1)

# cake1 = project1.Cake()
# cake1.generate_cake()
