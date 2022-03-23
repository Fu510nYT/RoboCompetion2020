#!/usr/bin/env python
import rospy
import time
import cv2
from open_manipulator_msgs.srv import SetJointPosition, SetJointPositionRequest, SetKinematicsPose, SetKinematicsPoseRequest
print("Successful in Importing")

#==============================================================================
def set_gripper(angle, t):
    service_name = "/goal_tool_control"
    rospy.wait_for_service(service_name)
    
    try:
        service = rospy.ServiceProxy(service_name,SetJointPosition)

        request = SetJointPositionRequest()
        request.joint_position.joint_name = ["gripper"]
        request.joint_position.position = [angle]
        request.path_time = t
        
        response = service(request)
        return response
    
    except Exception as e:
        rospy.loginfo("%s" % e)
        return False
def open_gripper(t):
    return set_gripper(0.01, t)

def close_gripper(t):
    return set_gripper(-0.01, t)


#===============================================================================

def move_to(x, y, z, t):
    service_name = "/goal_task_space_path_position_only"
    rospy.wait_for_service(service_name)
    
    try:
        service = rospy.ServiceProxy(service_name, SetKinematicsPose)
        
        request = SetKinematicsPoseRequest()
        request.end_effector_name = "gripper"
        request.kinematics_pose.pose.position.x = x
        request.kinematics_pose.pose.position.y = y
        request.kinematics_pose.pose.position.z = z
        request.path_time = t
        
        response = service(request)
        return response
    except Exception as e:
        rospy.loginfo("%s" % e)
        return False



if __name__ == "__main__":
    rospy.init_node("ros_tutorial")
    rospy.loginfo("ros_tutorial node start!")
    t = 1.0
    set_gripper(0.0, t)
    time.sleep(t)
    open_gripper(t)
    time.sleep(t)
    close_gripper(t)
    time.sleep(t)
    rospy.loginfo("Gripper Test Successful")
    xyz_init = (0.288, 0.0, 0.194)
    xyz_home = (0.134, 0.0, 0.240)
    t = 3.0
    move_to(xyz_home[0], xyz_home[1], xyz_home[2], t)
    time.sleep(t)
    move_to(xyz_init[0], xyz_init[1], xyz_init[2], t)
    time.sleep(t)
    move_to(xyz_home[0], xyz_home[1], xyz_home[2], t)
    time.sleep(t)
    rospy.loginfo("Movement test Successful")
    
    move_to(xyz_init[0], xyz_init[1], xyz_init[2], t)
    time.sleep(t)
    while not rospy.is_shutdown():
        rospy.Rate(1).sleep()
	rospy.loginfo(cv2.waitKey(0))
	if cv2.waitKey(0) in [97, ord("a")]:
            move_to(0.256, 0.132, 0.188, t)
            time.sleep(t)


    rospy.loginfo("ros_tutorial node end!")
