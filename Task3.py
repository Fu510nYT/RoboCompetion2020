#!/usr/bin/env python
import rospy
from mr_voice.msg import Voice
from std_msgs.msg import String
import requests
import datetime
import pyttsx3

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
def callback_voice(msg):
    global voice
    voice = msg
    rospy.loginfo("%s (%d)" % (voice.text, voice.direction))
    
if __name__ == "__main__":
    engine = pyttsx3.init()
    rospy.init_node("voicetest")
    rospy.loginfo("Initial Node Started")
    
    rospy.Subscriber("/voice/text", Voice, callback_voice)
    
    voice = None
    text1 = None
    
    have = False
    

    num = 0
    asked = False
    while not rospy.is_shutdown():
        
        rospy.Rate(20).sleep()
        
        
        try:
            question = qs[num].rstrip()
            reply = r[num].rstrip()
            reply_no = rn[num].rstrip()
        except:
         
            break
        
        if asked == False:
            print question
            asked = True
        
        
        if voice is not None:
            text = voice.text.lower()
    
            if "no" in text:
                print reply_no
                if num == 0:
                    records.write("False")
                    rec.write("Robot: Are you feeling better?")
                    rec.write("Patient: %s" % text)
                if num == 1:
                    records.write("False")
                    rec.write("Robot: Is the medicine working?")
                    rec.write("Patient: %s" % text)
                    
                voice = None
                
            else:
                print reply
                records.write("True")
                if num == 0:
                    rec.write("Robot: Are you feeling better?")
                    rec.write("Patient: %s" % text)
                
                if num == 1:
                    rec.write("Robot: Is the medicine working?")
                    rec.write("Patient: %s" % text)
                voice = None
            
            asked = False
            
            
            num += 1
        
