"""
Config file to store Global Variables
"""

from collections import deque

#Live Data Queue in which sensors push data
sensor_data_queue=deque()

#Buffered Data Queue
buffer_queue=deque()

#Incremental Variable to store sucesssfuly transmitted Requestes
transmitted=0

#Timer to read Sensor Data
sensor_time=60