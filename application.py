import datetime

import apihandler
import helper
from flask import Flask, render_template, request, flash

application = Flask(__name__)
application.secret_key = "cockandballs"
time_since_start = 0
session_id = 0
session_start_time = datetime.datetime.utcnow()


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

@application.route("/testsession", methods=["POST", "GET"])
def testsession():
    global session_id
    testsessionstring = apihandler.testSession(session_id)
    result = apihandler.requestFromAPI(testsessionstring)
    flash(result)
    return render_template("testsession.html")


@application.route("/check", methods=["POST", "GET"])
def check():
    global time_since_start
    global session_id
    global session_start_time
    time_since_start = apihandler.datetimenow() - session_start_time
    flash("Session ID: " + str(session_id))
    flash("Time since start: " + helper.timeDeltaToMinSec(str(time_since_start)))
    datausedcheck = apihandler.checkdatause(session_id)
    flash(datausedcheck)
    return render_template("check.html")


@application.route("/gods", methods=["POST", "GET"])
def gods():
    global time_since_start
    global session_id
    global session_start_time
    time_since_start = apihandler.datetimenow() - session_start_time
    flash("Session ID: " + str(session_id))
    flash("Session start time: " + str(session_start_time))
    flash("Time since start: " + helper.timeDeltaToMinSec(str(time_since_start)))
    gods_call_string = apihandler.callString(["getgods", "1"], session_id)
    god_data = apihandler.requestFromAPI(gods_call_string)
    assassins = list()
    guardians = list()
    hunters = list()
    mages = list()
    warriors = list()
    roles = [assassins, guardians, hunters, mages, warriors]
    for god in god_data:
        for role in roles:
            if god["Roles"] == role:
                role.append(god["Name"])
                break
    for role in roles:
        flash(role)
        for god in role:
            flash(god)
    return render_template("gods.html")
