#!/usr/bin/env python

import numpy as np
from AJTemplateBot.srv import Backward, BackwardResponse
import rospy
from std_msgs.msg import Float64

def backward_kinematics(req):
    d1 = 0.9
    d2 = 0.8
    d3 = 0.8
    x = req.x
    y = req.y
    z = req.z

    base = np.arctan2(y,x)
    r2 = x**2+y**2+(z-d1)**2
    elbow_val = ((d2**2+d3**2 )-r2)/(2*d2*d3)
    elbow = np.pi-np.arccos(elbow_val)
    shoulder = np.arcsin((z-d1)/np.sqrt(r2))+np.arctan2((d3*np.sin(elbow)),(d2+d3*np.cos(elbow)))
    shoulder = np.pi/2-shoulder

    base_publisher = rospy.Publisher('/AJBot/base_rotation_controller/command', Float64, queue_size=1)
    shoulder_publisher = rospy.Publisher('/AJBot/shoulder_rotation_controller/command', Float64, queue_size=1)
    elbow_publisher = rospy.Publisher('/AJBot/elbow_rotation_controller/command', Float64, queue_size=1)
    base_publisher.publish(base)
    shoulder_publisher.publish(shoulder)
    elbow_publisher.publish(elbow)

    resp = BackwardResponse()
    resp.t1 = base
    resp.t2 = shoulder
    resp.t3 = elbow
    return resp


def backward_server():
    rospy.init_node('backward_server')
    s = rospy.Service('backward', Backward , backward_kinematics)
    print('backward server is ready')
    rospy.spin()


if __name__ == "__main__":
    backward_server()

