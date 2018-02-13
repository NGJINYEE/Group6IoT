from flask import Flask, render_template, request, url_for, jsonify
import json

app = Flask(__name__)

#load home page
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

#Write to a simple database txt files for the colours received from the sensor
@app.route('/tests', methods=['POST'])
def my_test_endpoint():
    input_json = request.get_json(force=True)
    print('closest:', input_json["closest"], 'ori-color:', input_json["ori-color"])
    #Write to a txt file to save the colour data
    json.dump(input_json, open("simple-database.txt", 'w'))

    dictToReturn = {'Response': 'Receieved!'}
    return jsonify(dictToReturn)

#Send the data back to the browser when requested
@app.route('/load_color', methods=['POST'])
def load_color():
	#Retrieve the data back from the txt file in json format
    message = json.load(open('simple-database.txt'))
    ori_hex = message["ori-color"]
    closest_hex = message["closest"]
    if request.method == "POST":
        return jsonify(oriHex=ori_hex, closestHex=closest_hex)

if __name__ == '__main__':
    app.run(debug=True)
