#!/usr/bin/env python

import numpy as np
from AJTemplateBot.srv import Forward, ForwardResponse
import rospy
from std_msgs.msg import Float64
def forward_kinematics(req):

    l2 = 0.8
    l3 = 0.8
    t1 = req.a
    t2 = req.b
    t3 = req.c
    T01 = np.array([[1, 0 , 0, 0],
                    [0, 1 , 0, 0],
                    [0, 0, 1, 0.9],
                    [0, 0, 0, 1]])
    T12 = np.array([[np.cos(t1),-np.sin(t1),0, 0],
                    [np.sin(t1), np.cos(t1), 0 , 0],
                    [0, 0, 1 , 0],
                    [0, 0, 0, 1]])
    T23 = np.array([[np.cos(t2), 0, np.sin(t2), l2 * np.sin(t2)],
                    [0, 1, 0, 0],
                    [-np.sin(t2), 0, np.cos(t2), l2 * np.cos(t2)],
                    [0, 0, 0, 1]])
    T34 = np.array([[np.cos(t3), 0, np.sin(t3), l3 * np.sin(t3)],
                    [0, 1, 0, 0],
                    [-np.sin(t3), 0, np.cos(t3), l3 * np.cos(t3)],
                    [0, 0, 0, 1]])
    
    T = T01.dot(T12).dot(T23).dot(T34)
    pos = np.dot(T, np.array([0, 0,0, 1]))
    x = pos[0]
    y = pos[1]
    z = pos[2]

    base_publisher = rospy.Publisher('/AJBot/base_rotation_controller/command', Float64, queue_size=1)
    shoulder_publisher = rospy.Publisher('/AJBot/shoulder_rotation_controller/command', Float64, queue_size=1)
    elbow_publisher = rospy.Publisher('/AJBot/elbow_rotation_controller/command', Float64, queue_size=1)
    base_publisher.publish(t1)
    shoulder_publisher.publish(t2)
    elbow_publisher.publish(t3)

    resp = ForwardResponse()
    resp.x = x
    resp.y = y
    resp.z = z
    return resp


def forward_server():
    rospy.init_node('forward_server')
    s = rospy.Service('forward', Forward, forward_kinematics)
    print('forward server is ready')
    rospy.spin()


if __name__ == "__main__":
    forward_server()

