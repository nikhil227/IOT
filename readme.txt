Python Version Required: 3.6.8



Installation Steps
1) Install the requirements.txt file

2)In MQTT Broker folder run main_broker.py. This file will initialize the MQTT-Broker server

3)A CSV Log file will be generated at the same level folder structure


4)Next In MQTT-Pubisher run main_publisher.py in a diiferent Shell . This file will initialize the MQTT-Publisher service

5)MQTT transmitted and buffered messages count can be checked from an exposed API. For that open browser enter url localhost:5000/status.
Their you will be able to see live count of transmitted and buffered messages

5) Currently MQTT Broker is configured to run at localhost,9998 & in MQTT-Publisher is flask server is setup at localhost:5000 

