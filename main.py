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
def integration_time(value=None):
        value = min(614.4, max(2.4, value))
        cycles = int(value / 2.4)
        i2c.writeto_mem(41,0x81,bytearray([256 - cycles]))

def initialize():
    #Activate the sensor reading
    i2c.writeto_mem(41,0x80,bytearray([0x03]))
    integration_time(2.4)

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

def temperature_and_lux():
        r, g, b, c = getRed(),getGreen(),getBlue(),getIntensity()
        x = -0.14282 * r + 1.54924 * g + -0.95641 * b
        y = -0.32466 * r + 1.57837 * g + -0.73191 * b
        z = -0.68202 * r + 0.77073 * g +  0.56332 * b
        d = x + y + z
        n = (x / d - 0.3320) / (0.1858 - y / d)
        cct = 449.0 * n**3 + 3525.0 * n**2 + 6823.3 * n + 5520.33
        return cct, y

def colourValue(r,g,b):
    R=r/255
    G=g/255
    B=b/255
    minimum=min(R,G,B)
    maximum=max(R,G,B)
    L=(minimum+maximum)/2
    V=maximum
    delta=maximum-minimum
    K=1-maximum
    C=(1-R-K)/(1-K)
    M=(1-G-K)/(1-K)
    Y=(1-B-K)/(1-K)

    if delta==0:
      return(0,0,L*100,V*100,C,M,Y,K)
    else:
      S=delta/(1-abs(2*L-1))


    if R>G and R>B:
        Hue=60*(((G-B)/delta)%6)
    elif G>B:
        Hue=60*(2.0+(B-R)/(delta))
    else:
        Hue=60*(4.0+(R-G)/(delta))

    return Hue,S*100,L*100,V*100,C,M,Y,K

def get_colour():
    r=getRed()
    g=getGreen()
    b=getBlue()
    c=getIntensity()
    if c > 20000:
        red=min(255,int(5.5*r))
        green=min(255,int(5*g))
        blue=min(255,int(4.5*b))
    else:
        red=min(255,int(7*r))
        green=min(255,int(4.5*g))
        blue=min(255,int(4.5*b))
    return colourValue(red,green,blue),"{0:02x}{1:02x}{2:02x}".format(int(red),
                             int(green),
                             int(blue))


def html_rgb():
    r, g, b, c = getRed(),getGreen(),getBlue(),getIntensity()
    red = pow((int((r/c) * 256) / 255), 2.5) * 255
    green = pow((int((g/c) * 256) / 255), 2.5) * 255
    blue = pow((int((b/c) * 256) / 255), 2.5) * 255
    return red, green, blue

# def html_hex():
#     r, g, b = html_rgb()
#     return "{0:02x}{1:02x}{2:02x}".format(int(r),
#                              int(g),
#                              int(b))

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
    colour = get_colour()
    # hex = html_hex()
    tAndL = temperature_and_lux()
    data = {"Hue": colour[0][0], "Saturation": colour[0][1],
            "Lightness": colour[0][2],"Value": colour[0][3],
            "C":colour[0][4],"M":colour[0][5],"Y":colour[0][6],"K":colour[0][7],
            "hex": colour[1], "temperature": tAndL[0], "intensity": tAndL[1]}

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
    time.sleep(1)
    client.connect()
    time.sleep(1)
    while True:
        print('SwitchPin Value:', switchPin.value())
        if switchData() == True:
            sendData(client)
        time.sleep(1)

main()
