from flask import Flask, render_template, request, flash

application = Flask(__name__)
application.secret_key = "cockandballs"


@application.route("/")
def index():
    flash("Player name")
    return render_template("index.html")


@application.route("/player", methods=["POST", "GET"])
def player():
    flash("It was " + str(request.form["name_input"]))
    return render_template("index.html")
