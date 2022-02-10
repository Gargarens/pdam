import apihandler
import helper
from flask import Flask, render_template, request, flash

application = Flask(__name__)
application.secret_key = "cockandballs"
time_since_start = 0
session_id = 0
session_start_time = 0


@application.route("/")
def index():
    # flash("Player name")
    return render_template("index.html")


@application.route("/start", methods=["POST", "GET"])
def start():
    global time_since_start
    global session_id
    global session_start_time
    session_id, session_start_timestamp, session_start_time = apihandler.getSessionID()
    time_since_start = apihandler.datetimenow() - session_start_time
    flash("Session ID: " + str(session_id))
    flash("Session start time: " + str(session_start_time))
    flash("Time since start: " + helper.timeDeltaToMinSec(str(time_since_start)))
    return render_template("start.html")


@application.route("/check", methods=["POST", "GET"])
def check():
    global time_since_start
    global session_id
    global session_start_time
    time_since_start = apihandler.datetimenow() - session_start_time
    flash("Session ID: " + str(session_id))
    flash("Session start time: " + str(session_start_time))
    flash("Time since start: " + helper.timeDeltaToMinSec(str(time_since_start)))
    return render_template("check.html")

