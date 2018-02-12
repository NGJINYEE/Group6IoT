import paho.mqtt.client as mqtt
import json
import math

print("Hello World!")

colors = {"dark brown": '9a460e', "dark yellow": "ffbc00", "orange": "ff5600", "black": '000000', "white": 'ffffff', "red": 'ff2525', "green": '00ff00', "yellow": 'fff700', "blue": '2525a0', "purple": '8000ff'}
color_in_hsl = {"brown1": '20,100,20', "brown2": '20,100,25', "brown3": '20,100,30',
"brown4": '20,100,40', "brown5": '20,100,45',"yellow1": "48,100,50", "yellow2": "48,100,55", "yellow3": "48,100,65", "yellow4": "48,100,70", "yellow5": "48,100,75", "black": '0,0,0', "white": '0,0,100', "red1": '0,100,40', "red2": '0,100,50', "red3": '0,100,55', "red4": '0,100,65', "red5": '0,100,35',"green1": '120,100,10', "green2": '120,100,20', "green3": '120,100,30',
"green4": '120,100,40', "green5": '120,100,50',"blue1": '240,100,30', "blue2": '240,100,40', "blue3": '240,100,50', "blue4": '240,100,55', "blue5": '240,100,60', "purple1": '271,100,10', "purple2": '270,100,25', "purple3": '270,100,35', "purple4": '270,100,40', "purple5": '270,100,50'}

color_r = {"brown1": '662200', "brown2": '802b00', "brown3": '993300', "brown4": 'cc4400', "brown5": 'e64d00', "yellow1": "ffcc00", "yellow2": "ffd11a", "yellow3": "ffdb4d", "yellow4": "ffe066", "yellow5": "ffe680", "black": '000000', "red1": 'cc0000', "red2": 'ff0000', "red3": 'ff1a1a', "red4": 'ff4d4d', "red5": 'b30000',"red6": '990000', "red7": '800000'}
color_g = {"green1": '003300', "green2": '006600', "green3": '009900', "green4": '00cc00', "green5": '00ff00'}
color_b = {"blue1": '000099', "blue2": '0000cc', "blue3": '0000ff', "blue4": '1a1aff', "blue5": '3333ff', "purple1": '1a0033', "purple2": '400080', "purple3": '5900b3', "purple4": '6600cc', "purple5": '8000ff'}

def getClosestColor(hex_val):
    closest_color = list(color_r.keys())[0]
    closest_color2 = list(color_r.keys())[0]
    # hex_val = 'feb4a8'
    y = 255**2.0 + 255**2.0 + 255**2.0
    min_val = math.sqrt(y)
    min_val2 = math.sqrt(y)

    #color from sensor
        R = int(hex_val[:2], 16)
        G = int(hex_val[2:4], 16)
        B = int(hex_val[4:], 16)
    if(R>=G and R>=B):
        colors=color_r
    elif(G>=B):
        colors=color_g
    else:
        colors=color_b

    for color_name, color_value in colors.items():
        #color from data
        r = int(color_value[:2], 16)
        g = int(color_value[2:4], 16)
        b = int(color_value[4:], 16)



        #human eye sensitivity is 0.3 to red, 0.59 to green, and 0.11 to blue
        x = (r - R)**2.0 + (g - G)**2.0 + (b - B)**2.0
        diff = math.sqrt(x)
        diff2 = 0.3 * abs(r - R) + 0.59 * abs(g - G) + 0.11 * abs(b - B)

        # print ("Standard:", "R: ", r, "G: ", g, "B: ", b, "diff: ", diff)
        # print ("Data:", "R: ", R, "G: ", G, "B: ", B, "diff: ", diff, "color: ", color_name)
        if diff < min_val:
            min_val = diff
            closest_color = color_name
        if diff2 < min_val2:
            min_val2 = diff2
            closest_color2 = color_name
            closest_color2_value = color_value

    # dictToSend = "ff00ff"
    res = requests.post('http://127.0.0.1:5000/tests', json=closest_color2_value)
    print('response from server:', res.text)
    dictFromServer = res.json()

    print (hex_val, "is closest to color using square error:", closest_color,", value:" ,closest_color_value)
    print (hex_val, "is closest to color using eye sentivity:", closest_color2,", value:",closest_color2_value)

# 47.5* Hue, 28.75*Saturation + 23.75 * Lightness

def get_closest_color(hue, saturation, lightness):
    closest_color = list(colors.keys())[0]
    min_val = 47.5 * 360 + 28.75 * 100 + 23.75 * 100
    cloest_color_val = list(colors.values())[0]

    for color_name, color_value in color_in_hsl.items():
        #hsl from data
        h = int(color_value.split(',')[0])
        s = int(color_value.split(',')[1])
        l = int(color_value.split(',')[2])

        #color from sensor
        H = hue
        S = saturation
        L = lightness

        #human eye sensitivity is 0.3 to red, 0.59 to green, and 0.11 to blue
        diff = 47.5 * abs(h - H) + 0.59 * abs(s - S) + 0.11 * abs(l - L)

        # print ("Standard:", "R: ", r, "G: ", g, "B: ", b, "diff: ", diff)
        # print ("Data:", "R: ", R, "G: ", G, "B: ", B, "diff: ", diff, "color: ", color_name)
        if diff < min_val:
            min_val = diff
            closest_color = color_name
            closest_color

    print ('hue:', hue, 'saturation:', saturation, 'lightness:', lightness, "is closest to color:", closest_color)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code" + str(rc))
    client.subscribe("esys/Arcus/#")


def on_message(client, userdata, msg):
    # print(msg.topic + " " + str(msg.payload))
    color_hex_input = json.loads(msg.payload)
    hex_val = color_hex_input['hex']
    hue = color_hex_input['Hue']
    saturation = color_hex_input['Saturation']
    lightness = color_hex_input['Lightness']

    # int_from_hex = int(hex_val, 16)
    getClosestColor(hex_val)
    get_closest_color(hue, saturation, lightness)


client = mqtt.Client()
client.subscribe("esys/Arcus/color")
client.on_connect = on_connect
client.on_message = on_message
client.connect('192.168.0.10')

client.loop_forever()
