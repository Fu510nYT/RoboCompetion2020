#!/usr/bin/env python
import rospy
import time
import cv2
from sensor_msgs.msg import Image      
from cv_bridge import CvBridge
from std_msgs.msg import String
import numpy as np
from ARM import *


if __name__ == "__main__":
    rospy.init_node("Get_Medicine")
    medicine = open("/home/mustar/robotcompetition2022/medicine.txt")
    m = medicine.readlines()
    
    
    
    color = m[0].lower().strip()
    frame=None            
    
    t = 3.0
    
    rospy.loginfo("Moving to home pose")
    
    set_joints(0.00, -1.051, 0.368, 0.701, t)
    time.sleep(t)
    
    open_gripper(t)
    time.sleep(t)
    
    if color == "red":
        set_joints(2.707, -0.936, 1.351, 0.072, t)
        time.sleep(t)
        
        set_joints(2.761, -0.130, 1.103, -0.545, t)
        time.sleep(t)
        
        close_gripper(t)
        time.sleep(t)
        
        set_joints(2.796, -0.735, 0.347, 0.607, t)
        time.sleep(t)
        
        set_joints(0.00, -1.051, 0.368, 0.701, t)
        time.sleep(t)
        
        open_gripper(t)
        time.sleep(t)   
        
    if color == "yellow":
        set_joints(-2.721, -0.591, 1.362, -0.135, t)
        time.sleep(t)
        
        set_joints(-2.721, 0.025, 0.785, -0.110, t)
        time.sleep(t)
        
        close_gripper(t)
        time.sleep(t)
        
        set_joints(-2.720, -0.456, 0.380, 0.522, t)
        time.sleep(t)
        
        set_joints(0.00, -1.051, 0.368, 0.701, t)
        time.sleep(t)
        
        open_gripper(t)
        time.sleep(t)
        
    if color == "green":
        set_joints(3.112, -0.923, 1.278, 0.413, t)
        time.sleep(t)
        
        set_joints(3.109, -0.190, 1.129, -0.373, t)
        time.sleep(t)
        
        close_gripper(t)
        time.sleep(t)
        
        set_joints(3.117, -0.557, 0.387, 0.607, t)
        time.sleep(t)
        
        set_joints(0.00, -1.051, 0.368, 0.701, t)
        time.sleep(t)
        
        open_gripper(t)
