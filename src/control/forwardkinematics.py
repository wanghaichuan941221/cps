import math

def forward_kinematics(t2,t3,t4):
	L1 = 9
	L2 = 11.5
	L3 = 10
	
	x1 = L1*math.sin(t2)
	y1 = L1*math.cos(t2)
	x2 = P1x + L2*math.sin(t2 + t3)
	y2 = P1y + L2*math.cos(t2 + t3)
	x3 = P2x + L3*math.sin(t2 + t3 + t4)
	y3 = P2y + L3*math.cos(t2 + t3 + t4)
	
	return [[x1,y1],[x2,y2],[x3,y3]]

def get_distance(endeffector, box):
	distance = math.sqrt(((endeffector[0]-box[0])**2)+((endeffector[1]-box[1])**2))
	return distance
