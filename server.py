from flask import Flask, render_template, request, url_for, jsonify
# from flask_socketio import SocketIO, emit

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
    print('data from client:', input_json)
    f = open('simple-database.txt', 'w')
    f.write(str(input_json))
    f.close()
    dictToReturn = {'Response': 'Receieved!'}
    return jsonify(dictToReturn)

@app.route('/load_color', methods=['POST'])
def load_color():
    f = open('simple-database.txt', 'r')
    message = f.read()
    if request.method == "POST":
        return jsonify(hex=message)

# if __name__ == '__main__':
#     socketio.run(app)


# color = "Initial"
# @app.route('/', methods=['GET'])
# def hello():
#     return "Hello World!"


if __name__ == '__main__':
    app.run(debug=True)
