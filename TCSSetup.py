from machine import Pin,I2C
import machine
import ujson
import network
from umqtt.simple import MQTTClient
import time

#Test whether connected to script
print("Hello World!")

#Variable
# ourId = 'EEERover'
# ourPassword = 'exhibition'
ourId = "EEERover"
ourPassword = "exhibition"
CLIENT_ID = int.from_bytes(machine.unique_id(), 'big')
BROKER_ADDRESS = '192.168.0.10'
i2c = I2C(scl=Pin(5), sda=Pin(4), freq=100000)
switchPin = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP)
_CYCLES = (0, 1, 2, 3, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60)
topic = 'esys/Arcus/color'

#Functions
def initialize():
    #Activate the sensor reading
    i2c.writeto_mem(41,0x80,bytearray([0x03]))

def sensor_enable_all(interrupt,wait,RGBC,power):
    enable=interrupt<<4 | wait<<3 | RGBC <<1 | power
    i2c.writeto_mem(41,0x80,bytearray([enable]))

def sensor_disable():
    i2c.writeto_mem(41,0x80,bytearray([0x00]))

def persistence_register(cycle=None):
    if cycle not in _CYCLES:
            raise ValueError("cycle must be 0, 1, 2, 3, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55 or 60")
    else:
            i2c.writeto_mem(41,0x8C,bytearray([_CYCLES.index(cycle)]))

def interrupt_threshold(upper2,upper1,lower2,lower1):
    i2c.writeto_mem(41,0x84,bytearray([lower1]))
    i2c.writeto_mem(41,0x85,bytearray([lower2]))
    i2c.writeto_mem(41,0x86,bytearray([upper1]))
    i2c.writeto_mem(41,0x87,bytearray([upper2]))

def getGreen():
    green = i2c.readfrom_mem(41,0x98,2)
    return int.from_bytes(green,'little')

def getRed():
    red = i2c.readfrom_mem(41,0x96,2)
    return int.from_bytes(red,'little')

def getBlue():
    blue = i2c.readfrom_mem(41,0x9A,2)
    return int.from_bytes(blue,'little')

def getIntensity():
    clear = i2c.readfrom_mem(41,0x94,2)
    return int.from_bytes(clear,'little')

def read():
    green=getGreen()
    red=getRed()
    blue=getBlue()
    clear=getIntensity()
    return 'red: {} green: {} blue: {} intensity: {} valid: {}'.format(red,green,blue, clear,valid())      #1

def integration_time(value=None):
        value = min(614.4, max(2.4, value))
        cycles = int(value / 2.4)
        i2c.writeto_mem(41,0x81,bytearray([256 - cycles]))

def wait_time(value=None):
       value = min(614.4, max(2.4, value))
       cycles = int(value / 2.4)
       i2c.writeto_mem(41,0x83,bytearray([256 - cycles]))

def sensor_id():
      return i2c.readfrom_mem(41,0x92,1)

def status():
      return i2c.readfrom_mem(41,0x93,1)

def read_memory():
    return i2c.readfrom_mem(41,0x80,32)

def gain(gain):
    _GAINS = (1, 4, 16, 60)
    if gain not in _GAINS:
            raise ValueError("gain must be 1, 4, 16 or 60")
    else:
         i2c.writeto_mem(41,0x8F,bytearray([_GAINS.index(gain)]))

def wlong(wait_multiply_enable):
    if wait_multiply_enable == 1:
         i2c.writeto_mem(41,0x8D,bytearray([2]))
    elif wait_multiply_enable ==0:
        i2c.writeto_mem(41,0x8D,bytearray([0]))

def valid():
        return bool(int.from_bytes(status(),'big') & 0x01)

def clear_interrupt():
    i2c.writeto(41,bytearray([0xe6]))

def temperature_and_lux():
        r, g, b, c = getRed(),getGreen(),getBlue(),getIntensity()
        x = -0.14282 * r + 1.54924 * g + -0.95641 * b
        y = -0.32466 * r + 1.57837 * g + -0.73191 * b
        z = -0.68202 * r + 0.77073 * g +  0.56332 * b
        d = x + y + z
        n = (x / d - 0.3320) / (0.1858 - y / d)
        cct = 449.0 * n**3 + 3525.0 * n**2 + 6823.3 * n + 5520.33
        return cct, y

def get_rgb():
    r=getRed()
    g=getGreen()
    b=getBlue()
    c=getIntensity()
    red=min(255,int(2.1*r*256/c))
    green=min(255,int(1.7*g*256/c))
    blue=min(255,int(1.7*b*256/c))
    return r,g,b,c,"{0:02x}{1:02x}{2:02x}".format(int(red),
                             int(green),
                             int(blue))

def html_rgb():
    r, g, b, c = getRed(),getGreen(),getBlue(),getIntensity()
    red = pow((int((r/c) * 256) / 255), 2.5) * 255
    green = pow((int((g/c) * 256) / 255), 2.5) * 255
    blue = pow((int((b/c) * 256) / 255), 2.5) * 255
    return red, green, blue

def html_hex():
    r, g, b = html_rgb()
    return "{0:02x}{1:02x}{2:02x}".format(int(r),
                             int(g),
                             int(b))

def toPayLoad(message):
    payload = ujson.dumps(message)
    return payload

def connectToWifi(id, password):
    ap_if = network.WLAN(network.AP_IF)
    ap_if.active(False)
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(id, password)
    status = sta_if.isconnected()
    print("Connection status:", status)
    client = MQTTClient(str(CLIENT_ID), BROKER_ADDRESS)
    return client

def publishMessage(client, topic, payload):
    client.publish(topic, bytes(payload, 'utf-8'))

#Need for while loop
def sendData(client):
    rgb = get_rgb()
    hex = html_hex()
    tAndL = temperature_and_lux()
    data = {"red": rgb[0], "green": rgb[1], "blue": rgb[2], "hex": rgb[4], "temperature": tAndL[0], "intensity": tAndL[1]}
    payload = toPayLoad(message=data)
    # client.publish(topic, bytes(paylod, 'utf-8'))
    publishMessage(client=client, topic=topic, payload=payload)

def switchData():
    if switchPin.value() == 0:
        return True
    elif switchPin.value() == 1:
        return False
#main
def main():
    initialize()
    #connect to client
    client = connectToWifi(id=ourId, password=ourPassword)
    client.connect()
    time.sleep(1)
    while True:
        print('SwitchPin Value:', switchPin.value())
        if switchData() == True:
            sendData(client)
        time.sleep(1)

main()
