import pixaltoangle

#  pixalcordinates = [0,300,450,450,600,300,450,450]
#  pixalcordinates = [150,150,450,300,450,450,300,600]

pixalcordinates_top = [0,300,450,450,600,300,450,150] # theta1 = (1/4)*pi and setpoint1 = -(1/4)*pi
#  pixalcordinates = [150,450,300,0,450,150,300,600]
pixalcordinates_side1 = [0,300,300,200,300,150,300,50,600,300]
calibration_distance_in_cm = 40
height_object_in_cm = 5

print("theta1,setpoint1",pixaltoangle.get_theta1_setpoint1(pixal_cordinates_top))
print("theta2,theta3,theta4",pixaltoangle.get_theta234_side1(pixal_cordinates_side1))
print("distance",pixaltoangle.get_distance_to_object(pixalcordinates_top,pixalcordinates_side1,calibration_distance_in_cm,height_object_in_cm))