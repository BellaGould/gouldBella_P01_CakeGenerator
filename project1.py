import maya.cmds as cmds
# cake generator!
# parameters: cake levels (integer), cake height (float), cake width (float),
# cake color (???), icing (boolean), cake level proportion (float)
# first I need to get Maya to generate a cylinder.
# We'll call this function generate_level


class Cake():
    def generate_level(self, level_width, level_height, level):
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
        icing_name = cmds.polyTorus(radius=level_width, sectionRadius=0.1)[0]
        cmds.xform(icing_name, translation=[0,
                   level_lift+level_height, 0])
        return icing_name

    def calculate_width(self, level, cake_width, level_proportion):
        # this is where we apply the level_proportion to the cake level.
        # we want the levels to get progressively smaller as they increase.
        # on level 0, we want the width to be unchanged.
        # level_width = cake_width
        level_width = (level_proportion**level)*cake_width
        return level_width

# I'll need to call generate_level multiple times.
# I can call this in another function, generate_cake.
    def generate_cake(self, levels=3, cake_height=3.0, cake_width=1.0,
                      level_proportion=0.75, cake_color="white", icing=True):
        cake_list = []
        level_height = cake_height/float(levels)
        for level in range(0, levels):
            level_width = Cake.calculate_width(self, level, cake_width,
                                               level_proportion)
            lvl_name = Cake.generate_level(self, level_width,
                                           level_height, level)
            cake_list.append(lvl_name)
            if icing is True:
                icing_name = Cake.generate_icing(self, level_width,
                                                 level_height, level)
                cake_list.append(icing_name)

    def _freeze_transforms(self, obj_name):
        cmds.makeIdentity(obj_name, apply=True, translate=True,
                          rotate=True, scale=True, normal=False,
                          preserveNormals=True)
