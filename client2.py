import paho.mqtt.client as mqtt
import json
import math
import requests

print("Hello World!")

color={"darkblue1":'204060',"darkblue":'000020',"darkgreen":'002000',"green":'002020',"brown":'200000',"purple":'200020',"black":'000000',"purple1":'000040',"blue1":'000080',"blue2":'0000c0',"blue3":'0000ff',"green1":'004000',"green2":'004040',"blue4":'004080',"blue5":'0040c0',"blue6":'0040ff',"green3":'008000',"green4":'008040',"cyan1":'008080',"blue7":'0080c0',"blue8":'0080ff',"green5":'00c000',"green6":'00c040',"green7":'00c080',"cyan2":'00c0c0',"blue9":'00c0ff',"green8":'00ff00',"green9":'00ff40',"green10":'00ff80',"cyan3":'00ffc0',"cyan4":'00ffff',"brown1":'400000',"purple2":'400040',"purple3":'400080',"purple4":'4000c0',"blue10":'4000ff',"green11":'404000',"purple5":'404080',"purple6":'4040c0',"purple7":'4040ff',"green12":'408000',"green13":'408040',"cyan5":'408080',"blue11":'4080c0',"blue12":'4080ff',"green14":'40c000',"green15":'40c040',"green16":'40c080',"cyan6":'40c0c0',"blue13":'40c0ff',"green17":'40ff00',"green18":'40ff40',"green19":'40ff80',"cyan7":'40ffc0',"cyan8":'40ffff',"red1":'800000',"red2":'800040',"purple8":'800080',"purple9":'8000c0',"purple10":'8000ff',"brown2":'804000',"brown3":'804040',"purple11":'804080',"purple12":'8040c0',"purple13":'8040ff',"green20":'808000',"green21":'808040',"purple14":'8080c0',"purple15":'8080ff',"green22":'80c000',"green23":'80c040',"green24":'80c080',"cyan9":'80c0c0',"blue14":'80c0ff',"green25":'80ff00',"green26":'80ff40',"green27":'80ff80',"cyan10":'80ffc0',"cyan11":'80ffff',"red3":'c00000',"red4":'c00040',"pink1":'c00080',"pink2":'c000c0',"pink3":'c000ff',"brown4":'c04000',"brown5":'c04040',"pink4":'c04080',"pink5":'c040c0',"pink6":'c040ff',"yellow1":'c08000',"brown6":'c08040',"brown7":'c08080',"purple16":'c080c0',"purple17":'c080ff',"yellow2":'c0c000',"yellow3":'c0c040',"yellow4":'c0c080',"gray3":'c0c0c0',"blue15":'c0c0ff',"yellow5":'c0ff00',"yellow6":'c0ff40',"green28":'c0ff80',"green29":'c0ffc0',"blue16":'c0ffff',"red5":'ff0000',"red6":'ff0040',"pink7":'ff0080',"pink8":'ff00c0',"pink9":'ff00ff',"orange1":'ff4000',"red7":'ff4040',"pink10":'ff4080',"pink11":'ff40c0',"pink12":'ff40ff',"yelloworange":'ff8000',"orange2":'ff8040',"red8":'ff8080',"pink13":'ff80c0',"pink14":'ff80ff',"yellow7":'ffc000',"yellow8":'ffc040',"yellow9":'ffc080',"red9":'ffc0c0',"purple18":'ffc0ff',"yellow10":'ffff00',"yellow11":'ffff40',"yellow12":'ffff80',"yellow13":'ffffc0',"white":'ffffff'}

color_in_hsl = {"dark brown": '24,83,33', "dark yellow": "44,100,50", "orange": "24,100,46", "black": '0,0,0', "white": '0,0,100', "red": '0,100,57', "green": '120,100,50', "yellow": '58,100,50', "blue": '240,62,39', "purple": '270,100,50'}

def getClosestColor(hex_val):
    closest_color = list(color.keys())[0]
    y = 255**2.0 + 255**2.0 + 255**2.0
    min_val = math.sqrt(y)

    #color from sensor
    R = int(hex_val[:2], 16)
    G = int(hex_val[2:4], 16)
    B = int(hex_val[4:], 16)


    for color_name, color_value in color.items():
        #color from data
        r = int(color_value[:2], 16)
        g = int(color_value[2:4], 16)
        b = int(color_value[4:], 16)

        #square error
        x = (r - R) ** 2.0 + (g - G) ** 2.0 + (b - B) ** 2.0
        diff = math.sqrt(x)

        # print ("Standard:", "R: ", r, "G: ", g, "B: ", b, "diff: ", diff)
        # print ("Data:", "R: ", R, "G: ", G, "B: ", B, "diff: ", diff, "color: ", color_name)
        if diff < min_val:
            min_val = diff
            closest_color = color_name
            closest_color_value = color_value

    print (hex_val, "is closest to color:", closest_color, ", value:" , closest_color_value)

    closest_color = str(closest_color_value)
    your_color = hex_val
    data_to_send = {'closest': closest_color, 'ori-color': your_color}
    res = requests.post('http://127.0.0.1:5000/tests', json=data_to_send)
    print('response from server:', res.text)
    dictFromServer = res.json()


def get_closest_color(hue, saturation, lightness):
    closest_color = list(color_in_hsl.keys())[0]
    min_val = 47.5 * 100 + 28.75 * 100 + 23.75 * 100

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
        diff = 47.5 * abs(h - H) / 3.6 + 28.75 * abs(s - S) + 23.75 * abs(l - L)

        if diff < min_val:
            min_val = diff
            closest_color = color_name

    print ('hue:', hue, 'saturation:', saturation, 'lightness:', lightness, "is closest to color:", closest_color)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code" + str(rc))
    client.subscribe("esys/Arcus/#")

def on_message(client, userdata, msg):
    color_hex_input = json.loads(msg.payload)
    hex_val = color_hex_input['hex']
    hue = color_hex_input['Hue']
    saturation = color_hex_input['Saturation']
    lightness = color_hex_input['Lightness']

    getClosestColor(hex_val)
    get_closest_color(hue, saturation, lightness)

client = mqtt.Client()
client.subscribe("esys/Arcus/color")
client.on_connect = on_connect
client.on_message = on_message
client.connect('192.168.0.10')

client.loop_forever()
