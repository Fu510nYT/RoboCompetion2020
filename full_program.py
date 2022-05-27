#!/usr/bin/env python
from GetMedicine import get_medicine
import rospy
import time
import cv2
from sensor_msgs.msg import Image, Imu      
from mr_voice.msg import Voice
from cv_bridge import CvBridge
from std_msgs.msg import String
import numpy as np
from robot_vision_msgs.msg import BoundingBoxes
from ARM import *
from geometry_msgs.msg import Twist
from RobotChassis import RobotChassis
from VoiceTest import task3
from tf.transformations import euler_from_quaternion
import datetime
#from chassis import *
#from turtlebotnode import *

def imu_callback(data):
    global _imu
    _imu = data

def say(text):
    global _pub_speaker
    _pub_speaker.publish(text)
    rospy.sleep(1)
    


def callback_voice(msg):
    global _voice
    _voice = msg
    rospy.loginfo("%s (%d)" % (_voice.text, _voice.direction))
    
def callback_image(msg):
    global _frame
    _frame = CvBridge().imgmsg_to_cv2(msg, "bgr8")


def callback_boxes(msg):
    global _boxes
    _boxes = msg.bounding_boxes

def callback_string(msg):
    global s
    rospy.loginfo(msg.data)
    s=msg.data
    
def callback_depth(msg):
    global _depth
    _depth = CvBridge().imgmsg_to_cv2(msg, "passthrough")

if __name__ == "__main__":
    
    #Connecting to hardware
    
    rospy.init_node("full_program")
    rospy.loginfo("Full Program Node Started!")
    
    _frame = None
    rospy.Subscriber("/camera/rgb/image_raw", Image, callback_image)
    
    _boxes = None
    rospy.Subscriber("/yolo_ros/bounding_boxes", BoundingBoxes, callback_boxes)
    
    _voice = None
    rospy.Subscriber("/voice/text", Voice, callback_voice)
    
    _msg_cmd_vel = Twist()
    _pub_cmd_vel = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
    
    _pub_speaker = rospy.Publisher("/speaker/say", String, queue_size=10)
    
    _depth = None
    rospy.Subscriber("/camera/depth/image_raw", Image, callback_depth)
    
    _imu = None
    rospy.Subscriber("/imu/data", Imu, imu_callback, queue_size=10)
    rospy.sleep(1)
    
    
    #setting parameters for task 1 (Get Medicine)
    
    medicine = open("/home/mustar/robotcompetition2022/medicine.txt")
    m = medicine.readlines()[0].lower().strip()
    
    #setting parameters for task 2 (Find Item)
    
    _status = 0
    bottle_status = None #Position that the bottle is in (Left, Right, Middle)
    item_target = "bottle"
    turned_angle = 0
    bottle_coords_x = 0
    bottle_coords_y = 0
    distance = 0
    
    original_yaw = None
    q = [
            _imu.orientation.x,
            _imu.orientation.y,
            _imu.orientation.z,
            _imu.orientation.w
        ]
        
    roll, pitch, yaw = euler_from_quaternion(q)
    rospy.loginfo(yaw)
    original_yaw = yaw
    
    status1_said = False
    status6_said = False
    rospy.loginfo("Yaw: %.2f" % yaw)
    
    #setting parameters for task 3 (Situation)
    num = 0 

    now = datetime.datetime.now()

    situation = open("/home/mustar/robotcompetition2022/situation.txt", "a+")
    questions = open("/home/mustar/robotcompetition2022/questions.txt", "a+")
    replies = open("/home/mustar/robotcompetition2022/replies.txt", "a+")
    replies_no = open("/home/mustar/robotcompetition2022/replies_if_no.txt", "a+")
    records = open("/home/mustar/robotcompetition2022/voice_records.txt", "a+")
    rec = open("/home/mustar/robotcompetition2022/records.txt", "a+")

    qs = questions.readlines()
    r = replies.readlines()
    rn = replies_no.readlines()
    
    
    print qs
    print r
    print rn
    
    url = "http://127.0.0.1:5000/Situation"
    url_home = "http://127.0.0.1:5000/"
    
    asked = False
    have = False
    text1 = None
    
    rospy.sleep(1)

    #Task 1
    rospy.loginfo("Task 1 Started")
    say("Hello it is time to take your medicine")
    get_medicine(m, 3)
    rospy.loginfo("Task 1 Finish")
    
    #Task 2
    rospy.loginfo("Task 2 Started")
    
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
        if _imu is None:
            print "Imu None"
            continue
            
            
        
        
            
        if _status == 0:
            say("Hello, is there anything I can get for you?")
            time.sleep(1)
            _status = 1
            
            rospy.loginfo("Status: 0 -> 1")
            continue
            
        if _status == 1:
            if not status1_said: 
                say("Looking for item")
                status1_said = True
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
            say("I found the item and Im going to get it")
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
            move_to(0.122, 0.002, 0.083, 3)
            time.sleep(3)
            
            _status = 6
            continue
        
        if _status == 6:
           
           if not status6_said:
               say("Turning back to you")
               status6_said = True
            
           yaw1 = None
           q1 = [
               _imu.orientation.x,
               _imu.orientation.y,
               _imu.orientation.z,
               _imu.orientation.w
               ]
    
           roll1, pitch1, yaw1 = euler_from_quaternion(q1)
           
           if yaw1 < 0: yaw1 += 3.14 * 2
           
           rospy.loginfo("Yaw1: %.2f ; Original Yaw: %.2f" % (yaw1, original_yaw))          
           while abs(yaw1 - original_yaw) > 0.1 and _imu is not None:
           
               _msg_cmd_vel.linear.x = 0
               _msg_cmd_vel.angular.z = -0.1
               _pub_cmd_vel.publish(_msg_cmd_vel)
               
               q1 = [
                   _imu.orientation.x,
                   _imu.orientation.y,
                   _imu.orientation.z,
                   _imu.orientation.w
                   ]
        
               roll1, pitch1, yaw1 = euler_from_quaternion(q1)
               rospy.loginfo("Yaw1: %.2f ; Original Yaw: %.2f" % (yaw1, original_yaw))          
               
           rospy.loginfo("I arrived")
           _status = 7
        if _status == 7:
            set_joints(0, 0, 0, 0, 3)
            time.sleep(3)
            open_gripper(3)
            time.sleep(3)
            close_gripper(3)
            time.sleep(3)
            move_to(0.122, 0.002, 0.083, 3)
            time.sleep(3)
            
            
            
            print "task 2 finish"
            break
            
    #Task 3
    
    
    while not rospy.is_shutdown():
        rospy.Rate(20).sleep()
        
        #rospy.loginfo("Num %d" % num)
        
        #rospy.loginfo(_voice)
        question = qs[num].rstrip()
        #rospy.loginfo("Qs: %s" % qs)
        reply = r[num].rstrip()
        #rospy.loginfo("R: %s" % r)
        reply_no = rn[num].rstrip()
        #rospy.loginfo("RN : %s" % rn)
        
        if asked == False:
        
            say(question)
            print question
            
            asked = True
        
        if _voice is not None:
            text = _voice.text.lower()
            rospy.loginfo("Text %s" % text)
            if "no" in text:
                say(reply_no)
                if num == 0:
                    records.write("False")
                    rec.write("Robot: Are you feeling better?")
                    rec.write("Patient: %s" % text)
                elif num == 1:
                    records.write("False")
                    rec.write("Robot: Is the medicine working?")
                    rec.write("Patient: %s" % text)
                _voice = None
            
            else:             
                say(reply)   
                
                records.write("True")
                if num == 0:
                    rec.write("Robot: Are you feeling better?")
                    rec.write("Patient: %s" % text)
                    
                elif num == 1:
                    rec.write("Robot: Is the medicine working?")
                    rec.write("Patient: %s" % text)
                _voice = None
                
                
            asked = False
            num += 1    
            if num > 2:
                break
                
            
    
            
    rospy.loginfo("Full_program node end!")
    
        
    
    
    
