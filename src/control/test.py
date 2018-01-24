import pixaltoangle as pixaltoangle

#  pixalcordinates = [0,300,450,450,600,300,450,450]
#  pixalcordinates = [150,150,450,300,450,450,300,600]

# pixalcordinates_top = [0,300,450,450,600,300,450,150] # theta1 = (1/4)*pi and setpoint1 = -(1/4)*pi
pixalcordinates_top = [0,300,450,450,600,300,599,300] # theta1 = (1/4)*pi and setpoint1 = 0

#  pixalcordinates = [150,450,300,0,450,150,300,600]
# pixalcordinates_side1 = [0,300,300,200,300,150,300,50,600,300]  # theta2 = 0, theta3 = 0, theta4 = 0
 pixalcordinates_side1 = [0,300,400,300,450,300,599,300,600,300]  # theta2 = 1/2 * pi, theta3 = 0, theta4 = 0
# pixalcordinates_side1 = [0,300,300,200,300,150,150,150,600,300]  # theta2 = 0, theta3 = 0, theta4 = -1/2 * pi
# pixalcordinates_side1 = [0,300,375,225,450,150,525,75,600,300]  # theta2 = 1/4 * pi, theta3 = 0, theta4 = 0
#pixalcordinates_side1 = [0,300,375,225,300,150,375,75,600,300]  # theta2 = 1/4 * pi, theta3 = -1/2 * pi, theta4 = 1/2 * pi

calibration_distance_in_cm = 40
height_object_in_cm = 5

pixaltoangle.get_theta1_setpoint1(pixalcordinates_top)
pixaltoangle.get_theta234(pixalcordinates_side1)
print("distance",pixaltoangle.get_distance_to_object(pixalcordinates_top,pixalcordinates_side1,calibration_distance_in_cm,height_object_in_cm))