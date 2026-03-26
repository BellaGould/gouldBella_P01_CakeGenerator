import maya.cmds as cmds
# cake generator!
# parameters: cake levels (integer), cake height (float), cake width (float),
# cake color (???), icing (boolean), cake level proportion (float)
# first I need to get Maya to generate a cylinder.
# We'll call this function generate_level

def generate_level(level_width, level_height):
    lvl_name = cmds.polyCylinder(height=level_height, radius=(level_width/2))[0]
    return lvl_name

def generate_icing():
    pass
    return icing_name

def calculate_width(level, cake_width, level_proportion):
    # this is where we apply the level_proportion to the cake level.
    # we want the levels to get progressively smaller as they increase.
    # on level 0, we want the width to be unchanged.
    # level_width = cake_width
    if level == 0:
        level_width = cake_width
    else:
        level_width = level*level_proportion*cake_width
    return level_width

# I'll need to call generate_level multiple times.
# I can call this in another function, generate_cake.
def generate_cake(levels=3, cake_height=3.0, cake_width=1.0, 
                  level_proportion=0.75, cake_color="white", icing=False):
    cake_list= []
    level_height = cake_height/levels
    for level in range(0, levels):
        level_width = calculate_width(level, cake_width, level_proportion)
        lvl_name = generate_level(level_width, level_height)
        cake_list.append(lvl_name)
        if icing == True:
            icing_name = generate_icing(level_width, level_height):
            cake_list.append(icing_name)
