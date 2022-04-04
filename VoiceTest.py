#!/usr/bin/env python
import rospy
from mr_voice.msg import Voice
from std_msgs.msg import String
import requests


url = "http://127.0.0.1:5000/Voice"
def callback_voice(msg):
    global voice
    voice = msg
    rospy.loginfo("%s (%d)" % (voice.text, voice.direction))
    
if __name__ == "__main__":
    rospy.init_node("voicetest")
    rospy.loginfo("Initial Node Started")
    
    rospy.Subscriber("/voice/text", Voice, callback_voice)
    
    voice = None
    
    rospy.loginfo("Say smth")
    
    while not rospy.is_shutdown():
        rospy.Rate(20).sleep()
        if voice is not None: 
            text = voice.text.lower()
        
            rospy.loginfo("What you said was:    %s" % text)
            post = requests.post(url, data={"a": text})
            
            #rospy.loginfo(post.text)
            voice = None
            
    
