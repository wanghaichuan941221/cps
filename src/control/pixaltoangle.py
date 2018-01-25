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

def get_linear_line(x1, y1, x2, y2):
    delta_x = x2 - x1
    delta_y = y2 - y1

    try:
        a = delta_y / delta_x
    except ZeroDivisionError:
        if delta_y >= 0:
            a = 10000
        else:
            a = -10000
    b = y1 - a * x1
    return a, b

def get_theta1_setpoint1(pixal_cordinates_top):
    x4, y4 = get_xy_between_two_points(pixal_cordinates_top[4],pixal_cordinates_top[5],pixal_cordinates_top[0],pixal_cordinates_top[1])

    # take note of the fact that it if you want to know the angle P2P0P1 you have to fill in P0P2P1 or P0P1P2
    theta1 = angle(x4,y4,pixal_cordinates_top[2],pixal_cordinates_top[3],pixal_cordinates_top[4],pixal_cordinates_top[5])
    a,b = get_linear_line(pixal_cordinates_top[0],pixal_cordinates_top[1],pixal_cordinates_top[4],pixal_cordinates_top[5])
    if pixal_cordinates_top[3]<a * pixal_cordinates_top[2] + b:
        theta1 = -1*theta1

    setpoint1 = angle(x4,y4,pixal_cordinates_top[6],pixal_cordinates_top[7],pixal_cordinates_top[4],pixal_cordinates_top[5])
    if pixal_cordinates_top[7]<a * pixal_cordinates_top[2] + b:
        setpoint1 = -1*setpoint1

    return theta1,setpoint1


def get_theta234(pixal_cordinates):
    x6, y6 = get_xy_between_two_points(pixal_cordinates[8], pixal_cordinates[9], pixal_cordinates[0], pixal_cordinates[1])

    # take note of the fact that it if you want to know the angle P2P0P1 you have to fill in P0P2P1 or P0P1P2
    theta2_temp = angle(x6, y6, pixal_cordinates[2], pixal_cordinates[3], pixal_cordinates[8], pixal_cordinates[9])
    print("theta2_temp", theta2_temp)
    theta2 = (1/2)*math.pi-theta2_temp
    # if pixal_cordinates[2] < x6:
    #     theta2 = -1 * theta2


    theta3_temp = angle(pixal_cordinates[2], pixal_cordinates[3], x6, y6, pixal_cordinates[4], pixal_cordinates[5])
    theta3 = math.pi-theta3_temp
    a, b = get_linear_line(x6, y6, pixal_cordinates[2], pixal_cordinates[3])
    print("a,b", a, b)

    if pixal_cordinates[2]< x6:

        if pixal_cordinates[5] > (a * pixal_cordinates[4] + b):
            theta3 = -1 * theta3
    else:
        if pixal_cordinates[5] < (a * pixal_cordinates[4] + b):
            theta3 = -1 * theta3

    theta4_temp = angle(pixal_cordinates[4], pixal_cordinates[5], pixal_cordinates[2], pixal_cordinates[3], pixal_cordinates[6], pixal_cordinates[7])
    theta4 = math.pi-theta4_temp
    a, b = get_linear_line(pixal_cordinates[2], pixal_cordinates[3], pixal_cordinates[4], pixal_cordinates[5])
    print("a,b",a , b)

    if pixal_cordinates[4]< pixal_cordinates[2]:
        if pixal_cordinates[7] > (a * pixal_cordinates[6] + b):
            theta4 = -1 * theta4
    else:
        if pixal_cordinates[7] < (a * pixal_cordinates[6] + b):
            theta4 = -1 * theta4

    return theta2, theta3, theta4


def get_distance_to_object(pixal_cordinates_top,pixal_cordinates_side1,calibration_distance_in_cm,height_object_in_cm):
    x4, y4 = get_xy_between_two_points(pixal_cordinates_top[4],pixal_cordinates_top[5],pixal_cordinates_top[0],pixal_cordinates_top[1])
    x6, y6 = get_xy_between_two_points(pixal_cordinates_side1[8], pixal_cordinates_side1[9], pixal_cordinates_side1[0], pixal_cordinates_side1[1])

    multi1 = calibration_distance_in_cm/phytagoras(pixal_cordinates_top[0],pixal_cordinates_top[1],pixal_cordinates_top[4],pixal_cordinates_top[5])
    multi2 = phytagoras(pixal_cordinates_side1[0],pixal_cordinates_side1[1],pixal_cordinates_side1[8],pixal_cordinates_side1[9])/calibration_distance_in_cm

    tx = phytagoras(x4,y4,pixal_cordinates_top[6],pixal_cordinates_top[7])*multi1*multi2

    x_distance_to_object_in_side1_view = x6 + tx

    a,b = get_linear_line(pixal_cordinates_side1[0],pixal_cordinates_side1[1],pixal_cordinates_side1[8],pixal_cordinates_side1[9])

    ty = height_object_in_cm*multi2

    y_distance_to_object_in_side1_view = a*x_distance_to_object_in_side1_view + b - ty

    distance_to_object_in_cm =  phytagoras(x_distance_to_object_in_side1_view, y_distance_to_object_in_side1_view, pixal_cordinates_side1[6], pixal_cordinates_side1[7])/multi2
    return distance_to_object_in_cm, tx, ty


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