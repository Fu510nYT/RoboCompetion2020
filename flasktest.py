#!/usr/bin/env python
import rospy
import flask

from flask import Flask, request
app = Flask(__name__)


@app.route('/')
def test():
    f = open("/home/mustar/voice_records.txt", "r")
    lines = f.readlines()
    f.close()
    s = "<style>.row { margin-bottom: 20px; }</style><div class='messagebox'>"
    for line in lines:
        s += "<div class='row'>" + line + "</div>"
    s += "</div>"
    return s
    
    
@app.route("/Voice", methods=['GET', 'POST'])
def Voice():
    voice = request.form["a"]
    f = open("/home/mustar/voice_records.txt", "a+")
    f.write("%s: %s\n" % ("2022-04-04 21:00:00", voice))
    f.close()
    print voice
    return "OK"
    
app.run("127.0.0.1", debug=True)
