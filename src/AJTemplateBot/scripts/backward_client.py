#!/usr/bin/env python
from __future__ import print_function
import sys
import rospy
from AJTemplateBot.srv import *

def backward_client(x, y, z):
    rospy.wait_for_service('backward')
    try:
        backward = rospy.ServiceProxy('backward', Backward)
        resp = backward(x, y, z)
        return [resp.t1,resp.t2,resp.t3]
    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)

def usage():
    return "%s [x y z]"%sys.argv[0]

if __name__ == "__main__":
    if len(sys.argv) == 4:
        x = float(sys.argv[1])
        y = float(sys.argv[2])
        z = float(sys.argv[3])
    else:
        print(usage())
        sys.exit(1)
	'''
    if ( a>3.14 or a<-3.14):
        print('link 1 can take numbers between -3.14 and 3.14')
        sys.exit(1)
    if ( b>0.50 or b<0):
        print('link 2 can take numbers between 0 and 0.50')
        sys.exit(1)
    if ( c>0.75 or c<0):
        print('link 3 can take numbers between 0 and 0.75')
        sys.exit(1)
	'''
    print("Requesting backward-k of  (%s,%s,%s)"%(x, y, z))
    resp = backward_client(x, y, z)
    print("(%s %s %s)"%(resp[0],resp[1],resp[2]))
