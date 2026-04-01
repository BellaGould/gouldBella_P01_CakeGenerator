import maya.cmds as cmds

class Car():
    def generate_body(car_depth, car_height, car_width):
        body_name = cmds.polyCube(depth=car_depth, 
                                  height=car_height, width=car_width)[0]
        return body_name
    
    def generate_wheels(wheel_radius, wheel_height, car_width, car_depth):
        wheel1 = cmds.polyCylinder(height=wheel_height, radius=wheel_radius)
        cmds.xform(wheel1, translation=[car_width/2.0, 0, car_depth/2.0,])

    def is_odd(number):
        result = number%2
        return result

    def set_pivot_to_origin(self):
        pass

    def generate_car(self, car_depth=3, car_height=1, car_width=1, wheel_radius=0.25, wheel_height=0.25):
        car_list=[]
        body_name = Car.generate_body(car_depth, car_height, car_width)
        
        car_list.append(body_name)
        Car.generate_wheels(wheel_radius, wheel_height, car_width, car_depth)

        #use is_odd function?
        