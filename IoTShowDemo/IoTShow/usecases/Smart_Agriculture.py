import RPi.GPIO as GPIO
import time
import math
import requests, json
import urllib
import paho.mqtt.client as mqtt
import Adafruit_DHT
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import Adafruit_DHT

import subprocess
from subprocess import PIPE
spi_mods = subprocess.Popen(['sudo lsmod |grep spi_b*'], shell=True,stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT, bufsize=1,
                               universal_newlines=True)
output = spi_mods.communicate()[0]
spi_mod_name = output.split()[0]
print("SPI MOD = ",spi_mod_name)
result = subprocess.check_output(['sudo', 'rmmod', spi_mod_name])
result = subprocess.check_output(['sudo', 'modprobe', spi_mod_name])

import lcdlib1

Broker = "162.255.85.191"
port = 1883

moisture_value = 0.0

SPI_PORT   = 0
SPI_DEVICE = 0
client = mqtt.Client()

client.connect(Broker,port)
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE)) 
topic = "device/5ca3cb9ff1327c04c1ec1338"
lcdlib1.lcd_init()
try:
    while True:
    
        
        moisture_value = mcp.read_adc(1)
        
        print("soil Moisture Value : ")
    
        #moisture_percent = 100*float(moisture_value)/1024
        print(1023-moisture_value)
#        print(moisture_percent)
        #print "{0:.0f}%".format(moisture_value)
        if moisture_value < 100:
            print "Optimum Soil Moisture"
            print "Water pump is OFF..."
        else:
            print "Water pump is ON..."
            time.sleep(5)
#       lcdlib.lcd_string("GEOFF",0x80)
        lcdlib1.lcd_string("Soil Moist:"+str(1023-moisture_value),0x80)


        data=json.dumps([{"sensor": "sc-agriculture",  "value":int(1023-moisture_value), "timestamp":"", "context":"Fire Flame!"}
            ])

        client.publish(topic,data)
        print("")
        print("Published data to cloud")
        print("")
        print("")
        time.sleep(5)
     
except TypeError:
       print ("type error")
except KeyboardInterrupt:
       print ("IO Error")
       GPIO.cleanup()
