import sys
import Adafruit_DHT
import time
import requests
from wyliodrin import *
import struct

alarm="off"

def colorToRGB (color):
  return struct.unpack ('BBB', color[1:].decode('hex'))

def basic_color (color):
  value = 0
  if color>=128:
    value = 1
  else:
    value = 0
  return value

# Parse command line parameters.
sensor_args = { '11': Adafruit_DHT.DHT11,
                '22': Adafruit_DHT.DHT22,
                '2302': Adafruit_DHT.AM2302 }
sensor = 22
pin = 17

pinMode (3, 1)

pinMode (2, 1)

pinMode (1, 1)

pinMode (4, 1)
# Try to grab a sensor reading.  Use the read_retry method which will retry up
# to 15 times to get a sensor reading (waiting 2 seconds between each retry).
humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

# Un-comment the line below to convert the temperature to Fahrenheit.
# temperature = temperature * 9/5.0 + 32

# Note that sometimes you won't get a reading and
# the results will be null (because Linux can't
# guarantee the timing of calls to read the sensor).
# If this happens try again!
i=1
http_response = None


while (True):
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    if humidity is not None and temperature is not None:
      print(i)
      print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
      i=i+1
    else:
      print('Failed to get reading. Try again!')
    sendSignal('temp', temperature)
    sendSignal('humidity',humidity)
    if(temperature>26)&(humidity>80):
        color = colorToRGB ('#ff0000')
        digitalWrite (3, basic_color(color[0]))
        digitalWrite (2, basic_color(color[1]))
        digitalWrite (1, basic_color(color[2]))
        print('red')
    elif ((temperature>26)and(humidity<80)and(humidity>50)):
        color = colorToRGB ('#ffffff')
        digitalWrite (3, basic_color(color[0]))
        digitalWrite (2, basic_color(color[1]))
        digitalWrite (1, basic_color(color[2]))
        print('white')
    elif (temperature>26)and(humidity<50):
        color = colorToRGB ('#330000')
        digitalWrite (3, basic_color(color[0]))
        digitalWrite (2, basic_color(color[1]))
        digitalWrite (1, basic_color(color[2]))
        print('brown')
    elif (temperature<26)and(temperature>10)and(humidity>80):
        color = colorToRGB ('#ffff00')
        digitalWrite (3, basic_color(color[0]))
        digitalWrite (2, basic_color(color[1]))
        digitalWrite (1, basic_color(color[2]))
        print('yellow')
    elif (temperature<26)and(temperature>10)and(humidity<80)and(humidity>50):
        color = colorToRGB ('#009900')
        digitalWrite (3, basic_color(color[0]))
        digitalWrite (2, basic_color(color[1]))
        digitalWrite (1, basic_color(color[2]))
        print('green')
    elif (temperature<26)and(temperature>10)and(humidity<50):
        color = colorToRGB ('#ff99ff')
        digitalWrite (3, basic_color(color[0]))
        digitalWrite (2, basic_color(color[1]))
        digitalWrite (1, basic_color(color[2]))
        print('pink')
    elif (temperature<10)and(humidity>80):
        color = colorToRGB ('#330033')
        digitalWrite (3, basic_color(color[0]))
        digitalWrite (2, basic_color(color[1]))
        digitalWrite (1, basic_color(color[2]))
        print('purple')
    elif (temperature<10)and(humidity<80)and(humidity>50):
        color = colorToRGB ('#00cccc')
        digitalWrite (3, basic_color(color[0]))
        digitalWrite (2, basic_color(color[1]))
        digitalWrite (1, basic_color(color[2])) 
        print('light blue')
    elif (temperature<10)and(humidity<50):
        color = colorToRGB ('#000099')
        digitalWrite (3, basic_color(color[0]))
        digitalWrite (2, basic_color(color[1]))
        digitalWrite (1, basic_color(color[2]))
        print('blue')
        
    if (temperature<26)and(temperature>10)and(humidity<80)and(humidity>50): 
      alarm = "off"
      digitalWrite(4,0)
    else: 
      
      alarm = "on"
      digitalWrite(4,1)
    http_response = requests.post('http://192.168.1.102:1880/postImplementationProjectData', data = {'temperature': temperature, 'humidity': humidity,"alarm":alarm})
    print(http_response.text)
    time.sleep(2)