import math
def phytagoras(x1,y1,x2,y2):
    length = math.sqrt(math.pow((x1-x2),2)+math.pow((y1-y2),2))
    return length

def angle(x1,y1,x2,y2,x3,y3):
    l1 = phytagoras(x2,y2,x3,y3)
    l2 = phytagoras(x1,y1,x2,y2)
    l3 = phytagoras(x1,y1,x3,y3)
    omega = math.acos((math.pow(l2,2)+math.pow(l3,2)-math.pow(l1,2))/(2*l2*l3))
    return omega

def get_xy_between_two_points(x1,y1,x2,y2):
    x = (x1+x2)/2
    y = (y1+y2)/2
    return x,y

def get_theta1_setpoint1(pixal_cordinates_top):
    x4, y4 = get_xy_between_two_points(pixal_cordinates_top[4],pixal_cordinates_top[5],pixal_cordinates_top[0],pixal_cordinates_top[1])

    # take note of the fact that it if you want to know the angle P2P0P1 you have to fill in P0P2P1 or P0P1P2
    theta1 = angle(x4,y4,pixal_cordinates_top[2],pixal_cordinates_top[3],pixal_cordinates_top[4],pixal_cordinates_top[5])
    if pixal_cordinates_top[3]<pixal_cordinates_top[5]:
        theta1 = -1*theta1

    setpoint1 = angle(x4,y4,pixal_cordinates_top[6],pixal_cordinates_top[7],pixal_cordinates_top[4],pixal_cordinates_top[5])
    if pixal_cordinates_top[7]<pixal_cordinates_top[5]:
        setpoint1 = -1*setpoint1
    print("theta1, setpoint1", theta1,setpoint1)


    return theta1,setpoint1



def get_theta234_side1(pixal_cordinates_side1):
    x6, y6 = get_xy_between_two_points(pixal_cordinates_side1[8],pixal_cordinates_side1[9],pixal_cordinates_side1[0],pixal_cordinates_side1[1])

    # take note of the fact that it if you want to know the angle P2P0P1 you have to fill in P0P2P1 or P0P1P2
    theta2_temp = angle(x6,y6,pixal_cordinates_side1[2],pixal_cordinates_side1[3],pixal_cordinates_side1[8],pixal_cordinates_side1[9])
    theta2 = (1/2)*math.pi-theta2_temp

    theta3_temp = angle(pixal_cordinates_side1[2],pixal_cordinates_side1[3],x6,y6,pixal_cordinates_side1[4],pixal_cordinates_side1[5])
    theta3 = math.pi-theta3_temp

    theta4_temp = angle(pixal_cordinates_side1[4],pixal_cordinates_side1[5], pixal_cordinates_side1[2],pixal_cordinates_side1[3],pixal_cordinates_side1[6],pixal_cordinates_side1[7])
    theta4 = math.pi-theta4_temp
    return theta2, theta3, theta4


def forward_kinematics(t2, t3, t4):
    L1 = 9
    L2 = 11.5
    L3 = 10

    x1 = L1 * math.sin(t2)
    y1 = L1 * math.cos(t2)
    x2 = P1x + L2 * math.sin(t2 + t3)
    y2 = P1y + L2 * math.cos(t2 + t3)
    x3 = P2x + L3 * math.sin(t2 + t3 + t4)
    y3 = P2y + L3 * math.cos(t2 + t3 + t4)

    return [[x1, y1], [x2, y2], [x3, y3]]


def get_distance_to_object(pixal_cordinates_top,pixal_cordinates_side1,height):
    x4, y4 = get_xy_between_two_points(pixal_cordinates_top[4],pixal_cordinates_top[5],pixal_cordinates_top[0],pixal_cordinates_top[1])

    multi1 = calibration_distance/phytagoras(pixal_cordinates_top[0],pixal_cordinates_top[1],pixal_cordinates_top[4],pixal_cordinates_top[5])/phytagoras(pixal_cordinates_side1[0],pixal_cordinates_side1[1],pixal_cordinates_side1[8],pixal_cordinates_side1[9])
    x_distance_to_object_in_side1_view = phytagoras(x4,y4,pixal_cordinates_top[6],pixal_cordinates_top[7])*multi1
    y_distance_to_object_in_side1_view = height

    distance_to_object =  phytagoras(x_distance_to_object_in_side1_view, y_distance_to_object_in_side1_view, pixal_cordinates_side1[6], pixal_cordinates_side1[7])
    return distance_to_object
