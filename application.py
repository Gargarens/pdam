import datetime
import databasehandler
import apihandler
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


@application.route("/createtables", methods=["POST", "GET"])
def createtables():
    players = databasehandler.getplayers()
    columns = ["god", "conquest", "arena", "joust", "assault", "under30arena", "conquestranked", "under30conquest",
                 "under30joust", "joustranked", "slash", "duelranked"]
    for player in players:
        name = player[1]
        databasehandler.createtable(name, columns)
    return render_template("createtables.html")


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


@application.route("/arena", methods=["POST", "GET"])
def arena():
    global session_id
    playername = "creviceguy"
    date = "20220427"
    hour = "20"
    #arenadata = apihandler.getmatchidsbyqueue(435, date, hour, session_id)
    #print("Matches for " + date + ", hour " + hour + ":")
    #print(arenadata)
    return render_template("arena.html")


@application.route("/player", methods=["POST", "GET"])
def player():
    global session_id
    playername = "BigGirl2003"
    playerdata = apihandler.getplayer(playername, session_id)[0]
    playerid = playerdata["Id"]
    matchhistory = apihandler.getmatchhistory(playerid, session_id)
    arenamatches = []
    under30arenamatches = []
    for match in matchhistory:
        if match["Match_Queue_Id"] == 435:
            arenamatches.append(match)
        elif match["Match_Queue_Id"] == 10195:
            under30arenamatches.append(match)

    print("Found " + str(len(arenamatches)) + " arena matches and " + str(len(under30arenamatches)) + " under30arena matches for " + playername + ".")
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

    #databasehandler.createtable("gods (name, role, pantheon)")
    databasehandler.testtable("gods")

    return render_template("check.html")


@application.route("/gods", methods=["POST", "GET"])
def gods():
    global session_id
    gods_call_string = apihandler.callString(["getgods", "1"], session_id)
    god_data = apihandler.requestFromAPI(gods_call_string)
    dbdata = []
    assassins = list()
    guardians = list()
    hunters = list()
    mages = list()
    warriors = list()
    roles = [assassins, guardians, hunters, mages, warriors]
    for god in god_data:
        dbdata.append((god["Name"], god["Roles"], god["Pantheon"]))
    databasehandler.insertintotable(dbdata, "gods")
    # for role in roles:
    #     flash("ROLE")
    #     for god in role:
    #         flash(god["Name"])
    return render_template("gods.html")
