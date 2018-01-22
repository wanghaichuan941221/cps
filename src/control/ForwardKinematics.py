def ForwardKinematics(t2,t3,t4):
	L1 = 9
	L2 = 11.5
	L3 = 10
	
	x1 = L1*sin(t2)
	y1 = L1*cos(t2)
	x2 = P1x + L2*sin(t1 + t2)
	y2 = P1y + L2*cos(t1 + t2)
	x3 = P2x + L3*sin(t1 + t2 + t3)
	y3 = P2y + L3*cos(t1 + t2 + t3)
	
	return [[x1,y1],[x2,y2],[x3,y3]]


