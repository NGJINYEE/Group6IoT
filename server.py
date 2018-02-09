import sys
import getpass
import re

from flask import Flask, render_template, request, redirect, Response
from flask.json import jsonify
import random, json

app = Flask(__name__)
app.debug = True

@app.route('/')
def hello():
    return "Hello World!"

# @app.route('/receiver', methods = ['GET', 'POST'])
# def worker():
#     #read json + reply
#     data = request.get_json(force=True)
#     result = ''
#
#     for item in data:
#         #loop over every row
#         result += str(item['userPath']) + str(item['commitKey']) + '\n'
#
#     gitChange = gitShowResult(data)
#
#     return json.dumps(gitChange)

if __name__ == "__main__":
    app.run()
