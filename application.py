from flask import Flask

application = Flask(__name__)

@application.route("/<name>")
def index(name):
    return "<h1>index {}</h1>".format(name)

