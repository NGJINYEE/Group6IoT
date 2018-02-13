from flask import Flask, render_template, request, url_for, jsonify
import json

app = Flask(__name__)
# app.config['SECRET_KEY'] = 'secret!'
# socketio = SocketIO(app)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# @socketio.on('my event')
# def test_message(message):
#     emit('my response', {'data': 'got it!'})
#
@app.route('/tests', methods=['POST'])
def my_test_endpoint():
    color = 'test-color!'

    input_json = request.get_json(force=True)
    # force=True, above, is necessary if another developer
    # forgot to set the MIME type to 'application/json'
    print('closest:', input_json["closest"], 'ori-color:', input_json["ori-color"])
    # f = open('simple-database.txt', 'w')
    # f.write(str(input_json))
    json.dump(input_json, open("simple-database.txt", 'w'))
    # f.close()
    dictToReturn = {'Response': 'Receieved!'}
    return jsonify(dictToReturn)

@app.route('/load_color', methods=['POST'])
def load_color():
    # f = open('simple-database.txt', 'r')
    # d = f.read()
    message = json.load(open('simple-database.txt'))
    ori_hex = message["ori-color"]
    closest_hex = message["closest"]
    print(ori_hex, closest_hex)
    if request.method == "POST":
        return jsonify(oriHex=ori_hex, closestHex=closest_hex)

# if __name__ == '__main__':
#     socketio.run(app)


# color = "Initial"
# @app.route('/', methods=['GET'])
# def hello():
#     return "Hello World!"


if __name__ == '__main__':
    app.run(debug=True)
