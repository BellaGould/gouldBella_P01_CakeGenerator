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
    cake_red = 1.0
    cake_green = 1.0
    cake_blue = 1.0
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
        level_width = (self.level_proportion**level)*self.cake_width
        return level_width
    
    def color_cake(self, grp_name):
        material = cmds.shadingNode("lambert",
                                    name="cakeShader", asShader=True)
        sg = cmds.sets(name="%sSG" % "cakeShader",
                       empty=True, renderable=True, noSurfaceShader=True)
        cmds.connectAttr("%s.outColor" % material, "%s.surfaceShader" % sg)
        color = [self.cake_red, self.cake_green, self.cake_blue]
        cmds.setAttr(material + ".color",
                     color[0], color[1], color[2], type="double3")
        cmds.sets(grp_name, forceElement=sg)

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
        Cake.color_cake(self, grp_name)

    def _freeze_transforms(self, obj_name):
        cmds.makeIdentity(obj_name, apply=True, translate=True,
                          rotate=True, scale=True, normal=False,
                          preserveNormals=True)


class CakeWin(QtWidgets.QDialog):
    def __init__(self):
        super(CakeWin, self).__init__(parent=get_maya_main_win())
        self.cake = Cake()
        self.setWindowTitle("Cake Generator")
        self.resize(500, 500)
        self._define_widgets()
        self._layout_ui()
        self._connect_signals()

    def _define_widgets(self):
        self.icing_layout = QtWidgets.QHBoxLayout()
        self.icing_lbl = QtWidgets.QLabel("Add icing?")
        self.icing_checkbox = QtWidgets.QCheckBox()
        self.icing_layout.addWidget(self.icing_lbl)
        self.icing_layout.addWidget(self.icing_checkbox)

        self.level_layout = QtWidgets.QHBoxLayout()
        self.level_lbl = QtWidgets.QLabel("Levels")
        self.level_spnbx = QtWidgets.QSpinBox()
        self.level_slider = QtWidgets.QSlider()
        self.level_slider.setMinimum(1)
        self.level_slider.setMaximum(99)
        self.level_slider.setOrientation(1)
        self.level_layout.addWidget(self.level_lbl)
        self.level_layout.addWidget(self.level_spnbx)
        self.level_layout.addWidget(self.level_slider)

        self.cake_height_layout = QtWidgets.QHBoxLayout()
        self.cake_height_lbl = QtWidgets.QLabel("Cake Height")
        self.cake_height_dsb = QtWidgets.QDoubleSpinBox()
        self.cake_height_dsb.setMinimum(1.0)
        self.cake_height_dsb.setMaximum(100.0)
        self.cake_height_layout.addWidget(self.cake_height_lbl)
        self.cake_height_layout.addWidget(self.cake_height_dsb)

        self.cake_width_layout = QtWidgets.QHBoxLayout()
        self.cake_width_lbl = QtWidgets.QLabel("Cake Width")
        self.cake_width_dsb = QtWidgets.QDoubleSpinBox()
        self.cake_width_dsb.setMinimum(1.0)
        self.cake_width_dsb.setMaximum(100.0)
        self.cake_width_layout.addWidget(self.cake_height_lbl)
        self.cake_width_layout.addWidget(self.cake_height_dsb)

        self.cake_proportion_layout = QtWidgets.QHBoxLayout()
        self.cake_proportion_lbl = QtWidgets.QLabel("Level Proportion")
        self.cake_proportion_dsb = QtWidgets.QDoubleSpinBox()
        self.cake_proportion_dsb.setMinimum(0.2)
        self.cake_proportion_dsb.setMaximum(1.0)
        self.cake_proportion_layout.addWidget(self.cake_proportion_lbl)
        self.cake_proportion_layout.addWidget(self.cake_proportion_dsb)

        self.build_btn = QtWidgets.QPushButton("Bake a cake!")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")

        self._define_color_widgets()

    def _define_color_widgets(self):
        self.red_layout = QtWidgets.QHBoxLayout()
        self.red_lbl = QtWidgets.QLabel("R")
        self.red_dsb = QtWidgets.QDoubleSpinBox()
        self.red_dsb.setMinimum(0.0)
        self.red_dsb.setMaximum(1.0)
        self.red_slider = QtWidgets.QSlider()
        self.red_slider.setOrientation(1)
        self.red_slider.setMinimum(0.0)
        self.red_slider.setMaximum(1.0)
        self.red_layout.addWidget(self.red_lbl)
        self.red_layout.addWidget(self.red_slider)

        self.green_layout = QtWidgets.QHBoxLayout()
        self.green_lbl = QtWidgets.QLabel("G")
        self.green_dsb = QtWidgets.QDoubleSpinBox()
        self.green_dsb.setMinimum(0.0)
        self.green_dsb.setMaximum(1.0)
        self.green_slider = QtWidgets.QSlider()
        self.green_slider.setOrientation(1)
        self.green_slider.setMinimum(0.0)
        self.green_slider.setMaximum(1.0)
        self.green_layout.addWidget(self.green_lbl)
        self.green_layout.addWidget(self.green_slider)

        self.blue_layout = QtWidgets.QHBoxLayout()
        self.blue_lbl = QtWidgets.QLabel("G")
        self.blue_dsb = QtWidgets.QDoubleSpinBox()
        self.blue_dsb.setMinimum(0.0)
        self.blue_dsb.setMaximum(1.0)
        self.blue_slider = QtWidgets.QSlider()
        self.blue_slider.setOrientation(1)
        self.blue_slider.setMinimum(0.0)
        self.blue_slider.setMaximum(1.0)
        self.blue_layout.addWidget(self.blue_lbl)
        self.blue_layout.addWidget(self.blue_slider)

    def _layout_ui(self):
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.addWidget(self.icing_layout)
        self.main_layout.addWidget(self.level_layout)
        self.main_layout.addWidget(self.cake_height_layout)
        self.main_layout.addWidget(self.cake_width_layout)
        self.main_layout.addWidget(self.cake_proportion_layout)
        self.main_layout.addWidget(self.red_layout)
        self.main_layout.addWidget(self.green_layout)
        self.main_layout.addWidget(self.blue_layout)
        self.main_layout.addWidget(self.build_btn)
        self.main_layout.addWidget(self.cancel_btn)
        self.setLayout(self.main_layout)

    def _connect_signals(self):
        self.cancel_btn.clicked.connect(self.close)
        self.build_btn.clicked.connect(self.generate_cake)

        self.level_spnbx.valueChanged.connect(self.level_slider.setValue)
        self.level_slider.valueChanged.connect(self.level_spnbx.setValue)

        self.red_dsb.valueChanged.connect(self.red_slider.setValue)
        self.red_slider.valueChanged.connect(self.red_dsb.setValue)
        self.green_dsb.valueChanged.connect(self.green_slider.setValue)
        self.green_slider.valueChanged.connect(self.green_dsb.setValue)
        self.blue_dsb.valueChanged.connect(self.blue_slider.setValue)
        self.blue_slider.valueChanged.connect(self.blue_dsb.setValue)

    def generate_cake(self):
        self.cake.levels = self.level_spnbx.value()
        self.cake.cake_height = self.cake_height_dsb.value()
        self.cake.cake_width = self.cake_width_dsb.value()
        self.cake.level_proportion = self.cake_proportion_dsb.value()
        self.cake.cake_red = self.red_dsb.value()
        self.cake.cake_green = self.green_dsb.value()
        self.cake.cake_blue = self.blue_dsb.value()
        self.cake.icing = self.icing_checkbox.isChecked()

# in maya: create CakeWin object
# win = project1.CakeWin()
# win.show###

# in maya script editor:
# import project1
# import importlib
# importlib.reload(project1)

# cake1 = project1.Cake()
# cake1.generate_cake()
