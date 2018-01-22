def f():
    l1 = m.sqrt(m.pow((x2-x3),2)+m.pow((y2-y3),2))
    l2 = m.sqrt(m.pow((x1-x3),2)+m.pow((y1-y3),2))
    l3 = m.sqrt(m.pow((x1-x2),2)+m.pow((y1-y2),2))
    a = m.acos((m.pow(l2,2)+m.pow(l3,2)-m.pow(l1,2))/(2*l2*l3))
    print a
