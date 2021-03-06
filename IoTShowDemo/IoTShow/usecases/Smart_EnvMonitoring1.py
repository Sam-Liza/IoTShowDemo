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

#import lcdlib

GPIO.setmode(GPIO.BCM)

GPIO.setup(13,GPIO.IN)


sensor = Adafruit_DHT.DHT11
dht11_pin = 4  # The Temperatur And Humiduty Sensor goes on digital port 4.
light_sensor_pin = 13
Broker = "162.255.85.191"
port = 1883

temp=0.0
humidity = 0.0
light_value = 0
gas_value = 0.0


SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

myAPI = '67M4VWQI9AVB0BAG'
baseURL = 'https://api.thingspeak.com/update?api_key=%s' % myAPI
#lcdlib.lcd_init()
try:
    while True:
    
        #IR Snesor
        print("---------------------")
        print("start Reading sensor values....")
        humidity, temp = Adafruit_DHT.read_retry(sensor, dht11_pin)
        
        if math.isnan(temp) == False and math.isnan(humidity) == False:
            #print("Temparature and Humidity sensor value")
            print()
            print("Temparature = %.02f C"%(temp))
            print("--------")
            print()
            print("Humidity = %.02f%%"%(humidity))
            print("--------")
            
        light_value = GPIO.input(light_sensor_pin)
        if light_value==0 or light_value==1:    
            if light_value==0:
                print ('Light Detected')
            else:
                print ('Light Not Detected')
        print("---------------------")
          
        gas_value = mcp.read_adc(0)
        print("Gas Value : ")
        print(gas_value)
       
#       lcdlib.lcd_string("GEOFF",0x80)
        #lcdlib.lcd_string("T:"+str(temp)+"'C H:"+str(humidity)+"%",0x80)
        #lcdlib.lcd_string("L: "+str(light_value)+" G:"+str(gas_value)+"ppm",0xC0)

        conn = urllib.urlopen(baseURL + '&field1=%s&field2=%s&field3=%s&field5=%s' % (temp,humidity,light_value,gas_value)) 
        print("")
        print("Published data to cloud")
        print("")
        print("")
        time.sleep(15)
     
except TypeError:
       print ("type error")
except KeyboardInterrupt:
       print ("IO Error")
       GPIO.cleanup()
