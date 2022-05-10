#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Image
from robot_vision_msgs.msg import BoundingBoxes
from geometry_msgs.msg import Twist
from std_msgs.msg import String
from cv_bridge import CvBridge
from ARM import *

def callback_image(msg):
    global _frame
    _frame = CvBridge().imgmsg_to_cv2(msg, "bgr8")


def callback_boxes(msg):
    global _boxes
    _boxes = msg.bounding_boxes


def say(text):
    global _pub_speaker
    _pub_speaker.publish(text)
    rospy.sleep(1)
    

if __name__ == "__main__":
    rospy.init_node("demo")
    rospy.loginfo("demo node start!")
    
    _frame = None
    rospy.Subscriber("/camera/rgb/image_raw", Image, callback_image)
    
    _boxes = None
    rospy.Subscriber("/yolo_ros/bounding_boxes", BoundingBoxes, callback_boxes)
    
    _msg_cmd_vel = Twist()
    _pub_cmd_vel = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
    
    _pub_speaker = rospy.Publisher("/speaker/say", String, queue_size=10)
    
    _status = 0
    
    c_frame_x = 640 / 2
    c_frame_y = 480 / 2
    box_bottle = None
    
    bottle_status = None
    
    while not rospy.is_shutdown():
        rospy.Rate(20).sleep()
        if _frame is None: continue
        if _boxes is None: continue
        
        if _status == 0:
            say("I am ready")
            _status = 1
            continue
        
        if _status == 1:
            _msg_cmd_vel.linear.x = 0.0
            _msg_cmd_vel.angular.z = 0.1
            _pub_cmd_vel.publish(_msg_cmd_vel)
            
            for box in _boxes:
                if box.Class == "bottle":
                    _status = 2
                    
                    break
            if _status == 2: continue
        
        if _status == 2:
            _msg_cmd_vel.linear.x = 0.0
            _msg_cmd_vel.angular.z = 0.0
            _pub_cmd_vel.publish(_msg_cmd_vel)
            say("I found the bottle")
            _status = 3
            continue
        
        if _status == 3:
        
        
            for box in _boxes:
            
            
                cx = (box.xmax + box.xmin) // 2
                cy = (box.ymax + box.ymin) // 2
                
                rospy.loginfo("Cx: %d" % cx)
                
                if cx > 426:
                
                    _msg_cmd_vel.linear.x = 0.0
                    _msg_cmd_vel.angular.z = -0.1
                    _pub_cmd_vel.publish(_msg_cmd_vel)
                    
                    if bottle_status != "right":
                        print "right"
                        bottle_status = "right"
                        
                    
                
                elif cx < 213:
                    _msg_cmd_vel.linear.x = 0.0
                    _msg_cmd_vel.angular.z = 0.1
                    _pub_cmd_vel.publish(_msg_cmd_vel)
                    
                
                    if bottle_status != "left":
                        print "left"
                        bottle_status = "left"
                    
                    
                else:
                    _msg_cmd_vel.linear.x = 0.0
                    _msg_cmd_vel.angular.z = 0.0
                    _pub_cmd_vel.publish(_msg_cmd_vel)
                    if bottle_status != "mid":
                        print "mid"
                        bottle_status = "mid"
                    _status = 4
                    
                
                    
            continue
                
        
        
    rospy.loginfo("demo node END!")
    
