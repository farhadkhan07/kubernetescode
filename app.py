from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'This is my First test Project. Great team work......!'
