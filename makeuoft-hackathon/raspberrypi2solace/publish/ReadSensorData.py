import pyfirmata
import paho.mqtt.client as mqtt
import random
import json

from cellulariot import cellulariot
import time


board=pyfirmata.Arduino('/dev/ttyACM0')

handle_button=board.get_pin('d:6:i')
led_front=board.get_pin('d:7:o')
led_back=board.get_pin('d:8:o')
buzzer=board.get_pin('d:9:o')
theft_mode_button=board.get_pin('d:10:i')

toggle_status=False

node = cellulariot.CellularIoTApp()
node.setupGPIO()

node.disable()
time.sleep(1)
node.enable()
node.powerUp()

num = 6474607452

def publish(client,sensor,topic,qos,simulated_reading,trend):
    simulated_reading = simulated_reading + trend * random.normalvariate(0.01, 0.005)
    payload = {"timestamp": int(time.time()), "device": sensor, sensor: simulated_reading}
    jsonpayload_sensor = json.dumps(payload, indent=4)
    client.publish(topic, jsonpayload_sensor, qos=qos)
    print("Published to topic {}: \n{}".format(topic, jsonpayload_sensor))

def toggle():
    if(toggle_status):
        toggle_status=False;
    else:
        toggle_status=True;
        
def lightsOn(currX,prevX):
    if(currX-prevX < -200):
        led_back.write(1)
    else:
        led_back.write(0)

def getAccelX():
    stringToSplit=str(node.readAccel())
    return float(stringToSplit[stringToSplit.find(":")+1:stringToSplit.find(",")])

def emergency_lights_blink():
    led_front.write(1)
    delay(1)
    led_front.write(0)
    delay(0)

def init_solace():
    # Connection parms for Solace Event broker
    solace_url = "mr2j0vvhki1l0v.messaging.solace.cloud"
    solace_port = 20134 
    solace_user = "solace-cloud-client"
    solace_passwd = "2h06t5aepqtqi039g5da3df2ap"
    solace_clientid = "python_publisher"

    # Sensor Topics
    solace_topic_acceleration = "devices/acceleration/events"
    solace_topic_pressure = "devices/pressure/events"
    solace_topic_sox = "devices/sox/events"
    solace_topic_level = "devices/level/events"

    # Instantiate/connect to mqtt client
    client = mqtt.Client(solace_clientid)
    client.username_pw_set(username=solace_user, password=solace_passwd)
    print("Connecting to solace {}:{} as {}".format(solace_url, solace_port, solace_user))
    client.connect(solace_url, port=solace_port)
    client.loop_start()

def main():
    init_solace()
    prevX=0
    currX=0
    while(True):
        time.sleep(0.1)
        currX=getAccelX()
        lightsOn(currX,prevX)
        
        #In case of theft
        if(prevX - currX > 1000):
            buzzer.write(1)
            node.sendSMS(str(num),"Warning:Bike is being moved")
        prevX=currX
        publish(client, "acceleration in x dir", solace_topic_acceleration, 1, currX, 0)
    
if __name__=="__main__":
    main()
    

