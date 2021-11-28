from flask import Flask

app = Flask(__name__)

print('\nAll item data:')

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


