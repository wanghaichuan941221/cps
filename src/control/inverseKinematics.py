import math


def inverse_kinematics(theta2, theta3, theta4, tx, ty):
    t2 = theta2
    t3 = theta3
    t4 = theta4
    dt = .01
    for n in range(3000):
        try:
            w2 = math.atan(ty/tx)*(-3.0/2.0)+math.atan((math.cos(t2+t3)*2.3e1+math.cos(t2)*1.8e1)/(math.sin(t2+t3)*2.3e1+math.sin(t2)*1.8e1))*(3.0/2.0)-math.sqrt(abs(tx)**2+abs(ty)**2)*(3.0/5.0e1)+math.sqrt(abs(math.cos(t2+t3+t4))**2+abs(math.sin(t2+t3+t4))**2)*(3.0/5.0)+math.sqrt(abs(math.cos(t2+t3)*(2.3e1/2.0)+math.cos(t2)*9.0)**2+abs(math.sin(t2+t3)*(2.3e1/2.0)+math.sin(t2)*9.0)**2)*(3.0/5.0e1)
        except ZeroDivisionError:
            w2 = 10
        try:
            w3 = math.sqrt(abs(tx)**2+abs(ty)**2)*(-2.7e1/5.75e2)+math.sqrt(abs(math.cos(t2+t3+t4))**2+abs(math.sin(t2+t3+t4))**2)*(5.4e1/1.15e2)+math.sqrt(abs(math.cos(t2+t3)*(2.3e1/2.0)+math.cos(t2)*9.0)**2+abs(math.sin(t2+t3)*(2.3e1/2.0)+math.sin(t2)*9.0)**2)*(2.7e1/5.75e2)
        except ZeroDivisionError:
            w3 = 10
        try:
            w4 = math.atan(ty/tx)*-3.0+math.atan(math.cos(t2+t3+t4)/math.sin(t2+t3+t4))*3.0
        except ZeroDivisionError:
            w4 = 10
        t2 = t2+(w2*dt)
        t3 = t3+(w3*dt)
        t4 = t4+(w4*dt)
    return t2, t3, t4

