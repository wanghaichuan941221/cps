import math
def phytagoras(x1,y1,x2,y2):
    length = math.sqrt(math.pow((x1-x2),2)+math.pow((y1-y2),2))
    return length

def angle(x1,y1,x2,y2,x3,y3):
    l1 = phytagoras(x2,y2,x3,y3)
    l2 = phytagoras(x1,y1,x2,y2)
    l3 = phytagoras(x1,y1,x3,y3)
    try:
        omega = math.acos(min(1,max(-1,(math.pow(l2,2)+math.pow(l3,2)-math.pow(l1,2))/(2*l2*l3))))
    except ValueError:
        print("VERY STRANGE ERROR =============================================")
        print("VERY STRANGE ERROR =============================================")
        print("VERY STRANGE ERROR ", x1,y1,x2,y2,x3,y3)
        print("VERY STRANGE ERROR ", l1, l2, l3)
        print("VERY STRANGE ERROR =============================================")
        print("VERY STRANGE ERROR =============================================")
        raise ValueError("STOP")
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


def get_x_y_object(pixal_cordinates_top,calibration_distance_in_cm,height_object_in_cm):
    x4, y4 = get_xy_between_two_points(pixal_cordinates_top[4],pixal_cordinates_top[5],pixal_cordinates_top[0],pixal_cordinates_top[1])

    multi1 = calibration_distance_in_cm/phytagoras(pixal_cordinates_top[0],pixal_cordinates_top[1],pixal_cordinates_top[4],pixal_cordinates_top[5])

    tx = phytagoras(x4,y4,pixal_cordinates_top[6],pixal_cordinates_top[7])*multi1
    ty = height_object_in_cm

    return tx, ty

def get_coords_side_or_right(theta1):
    inverse_angles = False
    choose_side_camera = False

    if theta1 >= -(1/4)*math.pi and theta1< (1/4)*math.pi:
        inverse_angles = False
        choose_side_camera = True
    elif theta1 >= (1/4)*math.pi and theta1 < (3/4)*math.pi:
        inverse_angles = True
        choose_side_camera = False
    elif theta1 >= (3/4)*math.pi and theta1 < -(3/4)*math.pi:
        inverse_angles = True
        choose_side_camera = True
    elif theta1 >= -(3/4)*math.pi and theta1 < -(1/4)*math.pi:
        inverse_angles = False
        choose_side_camera = False
    else:
        raise ValueError("error: Theta1 should be between [-pi, pi]")

    return choose_side_camera, inverse_angles


def invserse_angles(theta2, theta3, theta4):
    return (-1)*theta2, (-1)*theta3, (-1)*theta4


def forward_kinematics(t2, t3, t4):
    L1 = 9
    L2 = 11.5
    L3 = 10

    x1 = L1 * math.sin(t2)
    y1 = L1 * math.cos(t2)
    x2 = x1 + L2 * math.sin(t2 + t3)
    y2 = y1 + L2 * math.cos(t2 + t3)
    x3 = x2 + L3 * math.sin(t2 + t3 + t4)
    y3 = y2 + L3 * math.cos(t2 + t3 + t4)

    return [[x1, y1], [x2, y2], [x3, y3]]