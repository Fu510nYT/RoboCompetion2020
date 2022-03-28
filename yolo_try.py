#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2, time
from robot_vision_msgs.msg import BoundingBoxes
from std_msgs.msg import String
from WASD import move_to, set_gripper, open_gripper, close_gripper

rospy.loginfo("Successful Import")

def callback_image(msg):
    global frame
    frame = CvBridge().imgmsg_to_cv2(msg, "bgr8")


def callback_boxes(msg):
    global boxes
    boxes = msg.bounding_boxes

def callback_string(msg):
    global s
    rospy.loginfo(msg.data)
    s=msg.data


if __name__ == "__main__":
    
    rospy.init_node("demo")
    rospy.loginfo("start!")
    s=""
    rospy.Subscriber("/record",String,callback_string)
    msg=rospy.Publisher("/say_something",String,queue_size=10)
    frame=None            
    rospy.Subscriber("/camera/rgb/image_raw", Image, callback_image)
    boxes = []
    rospy.Subscriber("/yolo_ros/bounding_boxes", BoundingBoxes, callback_boxes)

    #while s=="" and s not in ["tie","book","chair","sofa","chair","backpack","bed","suitcase","handbag","tvmoniter","remote","baseball bat","carrot","dining table","knife","cup","scissors","cell phone","toothbursh","skateboard","vase","keyboard","laptop","mouse","bottle"]:
        #pass
    s1 = "bottle"

    frames = []
    t = 3
    status = None
    while not rospy.is_shutdown():
        if frame is not None:
            frame2 = frame.copy()
            
            bottle_count = 0
            for box in boxes:
                
                if box.Class == s1:
                    bottle_count += 1
                    cx = (box.xmax + box.xmin) // 2
                    cy = (box.ymax + box.ymin) // 2
                    cv2.circle(frame2, (cx, cy), 5, (0, 0, 255), -1)
                    cv2.rectangle(frame2, (box.xmin, box.ymin), (box.xmax, box.ymax), (0, 255, 0), 2)
                    c_frame_x = 640 / 2
                    c_frame_y = 480 / 2
                    if cx > c_frame_x and (cx - c_frame_x > 100):
                        cv2.rectangle(frame2, (box.xmin, box.ymin), (box.xmax, box.ymax), (255, 0, 0), 2)
                        
                        rospy.loginfo("right ok")
                        msg.publish("The"+s1+" is on the right")
                        time.sleep(0.75)
			
			
			move_to(0.217, -0.178, 0.195, t)
			time.sleep(2)

			if status != "right":
				open_gripper(3)
				time.sleep(2)
				rospy.loginfo("Gripper Close")
				close_gripper(3)
				
			
			
				status = "right"
                    elif cx < c_frame_x and (c_frame_x - cx > 100):
                        cv2.rectangle(frame2, (box.xmin, box.ymin), (box.xmax, box.ymax), (0, 0, 255), 2)
                        
                        rospy.loginfo("left ok")
                        msg.publish("The"+s1+" is on the left")
                        time.sleep(0.75)
			
			move_to(0.217, 0.115, 0.187, t)
			time.sleep(2)			

			if status != "left":
				
				open_gripper(3)
				time.sleep(2)
				rospy.loginfo("Gripper Close")
				close_gripper(3)
				status = "left"


                    elif cx == c_frame_x or (c_frame_x - cx <= 100) or (cx - c_frame_x <= 100):
                        cv2.rectangle(frame2,(box.xmin, box.ymin), (box.xmax, box.ymax), (0, 255, 0), 2)
                        
                        rospy.loginfo("middle ok")
                        msg.publish("The"+s1+" is in the middle")
                        time.sleep(0.75)
				

            if bottle_count == 0:
               
                rospy.loginfo("no ok")
                msg.publish("There is no"+s1)
                time.sleep(0.75)
            cv2.imshow("frame", frame2)
            cv2.waitKey(1)

    move_to(0.134, 0.0, 0.240, t)
