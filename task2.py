#!/usr/bin/env python
from GetMedicine import get_medicine
import rospy
import time
import cv2
from sensor_msgs.msg import Image      
from cv_bridge import CvBridge
from std_msgs.msg import String
import numpy as np
from robot_vision_msgs.msg import BoundingBoxes
from ARM import *
from VoiceTest import *
from geometry_msgs.msg import Twist
from RobotChassis import RobotChassis


def say(text):
    global _pub_speaker
    _pub_speaker.publish(text)
    rospy.sleep(1)
    
def callback_image(msg):
    global _frame
    _frame = CvBridge().imgmsg_to_cv2(msg, "bgr8")
    
def callback_boxes(msg):
    global _boxes
    _boxes = msg.bounding_boxes                                 

def callback_string(msg):
    global s
    rospy.loginfo(msg.data)
    s = msg.data
    
def callback_depth(msg):
    global _depth
    _depth = CvBridge().imgmsg_to_cv2(msg, "passthrough")
    

if __name__ == "__main__":
    rospy.init_node("Task2")
    rospy.loginfo("Task 2 Start!")
    
    _frame = None
    rospy.Subscriber("/camera/rgb/image_raw", Image, callback_image)
    
    _boxes = None
    rospy.Subscriber("/yolo_ros/bounding_boxes", BoundingBoxes, callback_boxes)
    
    _msg_cmd_vel = Twist()
    _pub_cmd_vel = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
    
    _depth = None
    rospy.Subscriber("/camera/depth/image_raw", Image, callback_depth)
    
    _pub_speaker = rospy.Publisher("/speaker/say", String, queue_size=10)
    
    _status = 0
    item_target = "bottle"
    bottle_status = None
    
    rospy.loginfo("ready")
    
    while not rospy.is_shutdown():
        rospy.Rate(20).sleep()
        if _frame is None: 
            print "Frame none"
            continue
        if _boxes is None: 
            print "box none"
            continue
        if _depth is None:
            print "depth none" 
            continue 
        
        if _status == 0:
            print "Hello, is there anything I can get for you?"
            _status = 1
            
            rospy.loginfo("Status: 0 -> 1")
            continue
            
        if _status == 1:
            print "Status 1"
            _msg_cmd_vel.linear.x = 0.0
            _msg_cmd_vel.angular.z = 0.1
            _pub_cmd_vel.publish(_msg_cmd_vel)
            
            
            print "Searching for item"
            
            for box in _boxes:
                if box.Class == item_target:
                    _status = 2
                    rospy.loginfo("Status: 1 -> 2")
                    break
                     
        if _status == 2:
            _msg_cmd_vel.linear.x = 0.0
            _msg_cmd_vel.angular.z = 0.0
            _pub_cmd_vel.publish(_msg_cmd_vel)
            rospy.loginfo("I found the %s" % item_target)
            _status = 3
            rospy.loginfo("Status: 2-> 3")
            continue
        
        if _status == 3:
            cx, cy = None, None
            for box in _boxes:
            
                if box.Class == item_target:
                    cx = (box.xmax + box.xmin) // 2
                    cy = (box.ymax + box.ymin) // 2
                    break
            if cx is None: continue
            
            e = _frame.shape[1] // 2 - cx
            v = 0.0005 * e
            rospy.loginfo("e: %.2f, v: %.2f" % (e, v))
            
            _msg_cmd_vel.linear.x = 0.0
            _msg_cmd_vel.angular.z = v
            _pub_cmd_vel.publish(_msg_cmd_vel)
            
            if abs(e) < 5: 
                _status = 4
                rospy.loginfo("Status: 3 -> 4")
                continue
            
            rospy.loginfo("Cx: %d" % cx)

        
        
        if _status == 4:
            rospy.loginfo("hi")
            
            cx, cy = None, None
            for box in _boxes:
                if box.Class == item_target:
                    cx = (box.xmax + box.xmin) // 2
                    cy = (box.ymax + box.ymin) // 2
                    break
            if cx is None: continue
                    
            d = _depth[cy][cx]
            
            cv2.circle(_frame, (cx, cy), 5, (0, 255, 0), -1)
            rospy.loginfo("d: %.4f" % d)
            
            if d == 0: continue
            
            if d > 700:
                rospy.loginfo("Moving Forward")
                _msg_cmd_vel.linear.x = 0.05
                _msg_cmd_vel.angular.z = 0.0
                _pub_cmd_vel.publish(_msg_cmd_vel)
            
            else:
                _msg_cmd_vel.linear.x = 0.0
                _msg_cmd_vel.angular.z = 0.0
                _pub_cmd_vel.publish(_msg_cmd_vel)
                rospy.loginfo("Status: 4 -> 5")
                _status = 5
                    
                    
        if _status == 5:
            open_gripper(3)
            time.sleep(3)
            move_to(0.135, 0.00, 0.236, 3)
            time.sleep(3)
            move_to(0.189, 0.000, 0.148, 3)
            time.sleep(3)
            move_to(0.288, 0.000, 0.072, 3)
            time.sleep(3)
            close_gripper(3)
            time.sleep(3)
            move_to(0.189, 0.000, 0.148, 3)
            time.sleep(3)
            move_to(0.119, -0.0001, 0.089, 3)   
            time.sleep(3)
            
            
            _status = 6
            
             
        
        
        
        
