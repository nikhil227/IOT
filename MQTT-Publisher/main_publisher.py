"""
author@Nikhil Goel

MQTT Publisher with buffered data sample
"""

import random
import time
import cfg
import threading
import paho.mqtt.client as mqtt


# Current Connection with Broker status flag
connflag = False

# Stores Live Data Message id to check if message transmitted sucessfully or not
msg_id=None

# Stores Buffer Data Message id to check if message transmitted sucessfully or not
buffer_msd_id=None


def on_connect(client, userdata, flags, response_code):
    """
    callback function run after sucessfull connection established
    """
    global connflag
    connflag = True
    print("Connected with status: {0}".format(response_code))


def on_disconnect(client, userdata, response_code):
    global connflag
    if response_code != 0:
        connflag = False
        print("Client Got Disconnected")


def on_publish(client,userdata,result):
    """
    Callback function after publish
    """
    global msg_id,buffer_msd_id
    if userdata=="main_sensor_data_queue":
        msg_id=result
    elif userdata=="buffer_data_queue":
        buffer_msd_id=result
    print("userdata, usedata={}".format(userdata))
    print("data published, msg_id={}".format(msg_id))
    pass


def read_senor_data(event_obj,timeout):
    """
    Dummy function Sensor to generate Sensor reading
    """
    while True:
        cfg.sensor_data_queue.append(str({ "Timestamp":time.time(), "Value":random.randint(0,150),"Sensor":"Sensor-2"}))
        event_obj.wait(timeout)


def push_live_sensor_data(event_obj,timeout):
    """
    Push Live Data to broker
    :param event_obj: Threading Event
    :param timeout: Sleep time
    """
    global msg_id,connflag
    while True:
       # if connflag == True:
        if len(cfg.sensor_data_queue)!=0 and connflag == True :
            print("In main queue before publish")

            #User data Flag to match message_id is from live thread or buffer thread
            senor_connect.user_data_set("main_sensor_data_queue")

            (rc, mid) = senor_connect.publish("Sensor1topic/test",cfg.sensor_data_queue[0], 1)
            event_obj.wait(1)
            print("rc {} , msgid {}".format(rc,mid))
            if rc !=0:
                connflag=False
            elif rc == 0 and msg_id == mid:
                print("Live data pushed to broker")
                cfg.sensor_data_queue.popleft()
                cfg.transmitted+=1
            else:
                cfg.buffer_queue.append(cfg.sensor_data_queue[0])
                cfg.sensor_data_queue.popleft()
        elif cfg.sensor_data_queue and connflag == False:
            print("In main queue connection broken")
            cfg.buffer_queue.append(cfg.sensor_data_queue[0])
            cfg.sensor_data_queue.popleft()

        else:
            event_obj.wait(timeout)


def push_buffer_data(event_obj,timeout):
    """
    Push buffer data to broker
    :param event_obj: Threading Event
    :param timeout: Sleep Time
    """
    global connflag,buffer_msd_id
    while True:
        if connflag==True:
            if cfg.buffer_queue:

                # User data Flag to match message_id is from buffer data thread
                senor_connect.user_data_set("buffer_data_queue")
                (rc, mid) = senor_connect.publish("Sensor1topic/test",cfg.buffer_queue[0], 1)
                print("rc {} , msgid {}".format(rc,mid))
                event_obj.wait(1)
                if rc!=0:
                    connflag == True
                elif rc == 0 and buffer_msd_id == mid:
                    print("data pushed")
                    cfg.buffer_queue.popleft()
                    cfg.transmitted += 1
            else:
                event_obj.wait(timeout)
        else:
            event_obj.wait(timeout)


if __name__ == '__main__':
    senor_connect = mqtt.Client("sensor1")

    #MQTT Connection to broker
    senor_connect.connect('localhost', 9998)

    # On connect callback fuction
    senor_connect.on_connect = on_connect

    #On publish callback function
    senor_connect.on_publish = on_publish


    wait_time = threading.Event()
    flag=threading.Event()
    senor_connect.loop_start()

    # Thread to generate sensor data every 60 sec
    thread1 = threading.Thread(target=read_senor_data, args=(wait_time,cfg.sensor_time))

    #Thread to push sensor data to broker
    thread2= threading.Thread(target=push_live_sensor_data, args=(wait_time,5))

    #To maintain buffer data & push the same to broker
    thread3 = threading.Thread(target=push_buffer_data, args=(wait_time, 5))

    #Intitialising Threads
    thread1.start()
    thread2.start()
    thread3.start()

    #Exposed API to check sent request & pending Requests at localhost:5000
    from api import app
    app.run()