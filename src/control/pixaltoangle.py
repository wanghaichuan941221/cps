import math

def get_theta1_setpoint1(pixal_cordinates):
    x4 = (pixal_cordinates[0]-pixal_cordinates[4])/2
    y4 = (pixal_cordinates[1]-pixal_cordinates[5])/2

    x2 = pixal_cordinates[2] - x4
    y2 = pixal_cordinates[3] - y4

    x3 = pixal_cordinates[4] - x4
    y3 = pixal_cordinates[5] - y4

    alpha1 = math.atan(y2/x2)
    alpha2 = math.atan(y3/x3)
    theta1 = alpha1+alpha2

    xp = pixal_cordinates[6] - x4
    yp = pixal_cordinates[7] - y4

    alpha3 = math.atan(yp/xp)
    setpoint1 = alpha2 + alpha3


    '''    
    l1 = math.sqrt(math.pow((x2-x3),2)+math.pow((y2-y3),2))
    l2 = math.sqrt(math.pow((x1-x3),2)+math.pow((y1-y3),2))
    l3 = math.sqrt(math.pow((x1-x2),2)+math.pow((y1-y2),2))
    a = math.acos((math.pow(l2,2)+math.pow(l3,2)-math.pow(l1,2))/(2*l2*l3))
    '''
    print theta1, setpoint1

def get_real_distance_from_base_to_object(pixal_coridinates,calibration_distance,object_higth_in_cm):
    x13 = pixal_cordinates[0] - pixal_cordinates[4]
    multi = calibration_distance/x13
    x13_2 = (pixal_cordinates[0]-pixal_cordinates[4])/2
    y13_2= (pixal_cordinates[1]-pixal_cordinates[5])/2
    radius_from_base_to_object =  (math.sqrt(math.pow((pixal_coridinates[6]-x13_2),2)+math.pow((y13_2-pixal_coridinates[7]),2)))*multi
    object_cordinates = [0]*2
    object_cordinates[0]=radius_from_base_to_object
    object_cordinates[1]=object_higth_in_cm
    return object_cordinates


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


def get_distance(p1, p2):
    distance = math.sqrt(((p1[0] - p2[0]) ** 2) + ((p1[1] - p2[1]) ** 2))
    return distance

def get_distance_between_endeffector_and_object(t2_, t3_, t4_, pixal_coridinates_,calibration_distance_,object_higth_in_cm_):
    p1_, p2_, p3_ = forward_kinematics(t2_, t3_, t4_)
    pobject_ = get_real_distance_from_base_to_object(pixal_coridinates_,calibration_distance_,object_higth_in_cm_)
    distance_ =get_distance(p3_, pobject_)
    return distance_