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
    global session_id
    global time_since_start
    global session_start_time
    session_id, session_start_timestamp, session_start_time = apihandler.getSessionID()
    # time_since_start = apihandler.datetimenow() - session_start_time
    # flash("Session ID: " + str(session_id))
    # flash("Session start time: " + str(session_start_time))
    # flash("Time since start: " + helper.timeDeltaToMinSec(str(time_since_start)))
    return render_template("start.html")


@application.route("/player", methods=["POST", "GET"])
def player():
    global session_id
    playername = "creviceguy"
    playerdata = apihandler.getplayer(playername, session_id)[0]
    playerid = playerdata["Id"]
    print(apihandler.getmatchhistory(playerid, session_id))
    return render_template("player.html")


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
    datausedcheck = apihandler.checkdatause(session_id)[0]

    requestsLeft = datausedcheck['Request_Limit_Daily'] - datausedcheck['Total_Requests_Today']
    flash("Requests left: " + str(requestsLeft))

    activeSessions = datausedcheck['Active_Sessions']
    flash("Active sessions: " + str(activeSessions))

    sessionsLeft = datausedcheck['Session_Cap'] - datausedcheck['Total_Sessions_Today']
    flash("Sessions left: " + str(sessionsLeft))

    return render_template("check.html")


@application.route("/gods", methods=["POST", "GET"])
def gods():
    global session_id
    gods_call_string = apihandler.callString(["getgods", "1"], session_id)
    god_data = apihandler.requestFromAPI(gods_call_string)
    assassins = list()
    guardians = list()
    hunters = list()
    mages = list()
    warriors = list()
    roles = [assassins, guardians, hunters, mages, warriors]
    for god in god_data:
        role = (god["Roles"].lower())
        if role == "assassin":
            roles[0].append(god)
        elif role == "guardian":
            roles[1].append(god)
        elif role == "hunter":
            roles[2].append(god)
        elif role == "mage":
            roles[3].append(god)
        elif role == "warrior":
            roles[4].append(god)
        else:
            print("Role parsing error for " + god["Name"])
    for role in roles:
        flash("ROLE")
        for god in role:
            flash(god["Name"])
    return render_template("gods.html")
