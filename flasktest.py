#!/usr/bin/env python

import flask
import datetime
from flask import Flask, request, render_template  
app = Flask(__name__)




now = datetime.datetime.now()
date = now.strftime("%Y-%m-%d %H:%M:%S")


@app.route('/')
def test():
    
    data = {
       "time" : date,
    }
    return render_template("home_page.html", data=data)

@app.route('/my_test')
def my_test():
    
    f = open("/home/mustar/robotcompetition2022/voice_records.txt", "a+")
    lines = f.readlines()
    f.close()
    
    rec = open("/home/mustar/robotcompetition2022/records.txt", "a+")
    records = rec.readlines()
    rec.close()
    
    content = {
        "Time" : date,
        "Feeling Better" : lines[0].strip(),   
        "Medicine Working" : lines[1].strip(),
        "Records": records
        
        
    }


    return render_template("template.html", content=content)

app.run("127.0.0.1", 5000, debug=True)
