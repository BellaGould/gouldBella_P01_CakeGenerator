# cake generator!
# parameters: cake levels (integer), cake height (float), cake width (float),
# cake color (???), icing (boolean), cake level proportion (float)
# first I need to get Maya to generate a cylinder.
# We'll call this function generate_level

def generate_level(level_width, level_height):
    pass

def generate_icing():
    pass

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
def generate_cake(levels=1, cake_height=3.0, cake_width=1.0, 
                  level_proportion=0.75, cake_color="white", icing=False):
    for level in range(0, levels):
        level_width = calculate_width(level, cake_width, level_proportion)
        generate_level(level_width, cake_height)
        if icing == True:
            generate_icing():
