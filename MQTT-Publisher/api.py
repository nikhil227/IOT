"""
Flask Server to check status of Transmitted & Pending Requests
"""

from flask import Flask, render_template
import cfg

#Flask Object
app=Flask(__name__)

#(Service running at localhost:5000/status)
@app.route('/status')
def hello_world():
   transmitted_msg=cfg.transmitted

   #Calulation count of buffered requests pending at the moment
   buffer_queue_count=len(cfg.buffer_queue)

   return render_template('home.html', data1=transmitted_msg, data2=buffer_queue_count)
