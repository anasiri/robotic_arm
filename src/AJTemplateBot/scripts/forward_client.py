#!/usr/bin/env python
from __future__ import print_function
import sys
import rospy
from AJTemplateBot.srv import *

def forward_client(a, b , c):
    rospy.wait_for_service('forward')
    try:
        forward = rospy.ServiceProxy('forward', Forward)
        resp = forward(a, b,c)
        return [resp.x,resp.y,resp.z]
    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)

def usage():
    return "%s [a0 a1 a2]"%sys.argv[0]

if __name__ == "__main__":
    if len(sys.argv) == 4:
        a = float(sys.argv[1])
        b = float(sys.argv[2])
        c = float(sys.argv[3])
    else:
        print(usage())
        sys.exit(1)
    if ( a>3.14 or a<-3.14):
        print('link 1 can take numbers between -3.14 and 3.14')
        sys.exit(1)
    if ( b>0.50 or b<0):
        print('link 2 can take numbers between 0 and 0.50')
        sys.exit(1)
    if ( c>0.75 or c<0):
        print('link 3 can take numbers between 0 and 0.75')
        sys.exit(1)

    print("Requesting forward-k of  (%s,%s,%s)"%(a, b,c))
    resp = forward_client(a, b,c)
    print("(%s %s %s)"%(resp[0],resp[1],resp[2]))
